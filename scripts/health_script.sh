outputpath=$1
outputfile=$2

# Basic checks
echo " " >> $outputpath/$outputfile
echo "[health]" >> $outputpath/$outputfile
echo "name           = $0" >> $outputpath/$outputfile
echo "node_name      = $HOSTNAME" >> $outputpath/$outputfile
current_time=$(date +%s)
last_run_time=$(cat /tmp/diagnose/last_run)

# Health Check
#-------------------------------------------------------------------------------------
# Test for presence of IB card.
if /sbin/lspci | grep -i -q Infiniband; then
  IB_PRESENT=true
  echo "ib_present     = 1.0" >> $outputpath/$outputfile
else 
  IB_PRESENT=false
  echo "ib_present     = 0.0" >> $outputpath/$outputfile
fi

# Things I'll need. 
IBSTAT=/usr/sbin/ibstat
PERFQUERY=/usr/sbin/perfquery
DMIDECODE=/usr/sbin/dmidecode
IBDIAGSSUMFILE=/tmp/ib_diags_sum
DMESGFILE=/tmp/dmesg
OOMFLAG=/tmp/oom_flag
IPOIB_PING_TARGET=172.28.0.1

# Find my node defaults, no point continuing if these are missing.
# The sourced script should set values to check against.
DEFAULTS=/curc/torque/scripts/nodes/$(hostname -s | tr 'A-Z' 'a-z')
if [[ ! -f $DEFAULTS ]]; then
  echo "ERROR MISSING_DEFAULTS"
  exit 1
fi
. /curc/torque/scripts/nodes/$(hostname -s | tr 'A-Z' 'a-z')

# Current values for me are:
if [[ $IB_PRESENT == "true" ]]; then
  # Gather some IB values.
  IB_STATE=$($IBSTAT | awk '/State:/ {print $2}' | head -1)
  IB_LINK=$($IBSTAT | awk '/Physical state:/ {print $3}' | head -1)
  IB_RATE=$($IBSTAT | awk '/Rate:/ {print $2}' | head -1)

  # If a sum file exists, use it. Otherwise clear counters and start over.
  if [[ -f $IBDIAGSSUMFILE ]]; then 
    LAST_IB_DIAGSSUM=$(<$IBDIAGSSUMFILE)
  else
    $PERFQUERY --Reset_only
    echo "0" > $IBDIAGSSUMFILE
    LAST_IB_DIAGSSUM="0"
  fi
  # Collect sum of current counter values.
  IB_DIAGSSUM=$($PERFQUERY | tr '.' ' ' | awk '/Errors:/ { sum += $2 } END { print sum }')
  echo $IB_DIAGSSUM > $IBDIAGSSUMFILE
fi

# Check for out of memory problems, preserving dmesg as we go.
if [[ ! -e $OOMFLAG ]]; then
  echo "false" > $OOMFLAG
fi

if dmesg -c | tee -a $DMESGFILE | grep -q "Out of memory: Killed process" > /dev/null 2>&1 ; then 
  echo "true" > $OOMFLAG
fi

# Collect total memory
MEM_TOTAL=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
# Get dimm count and speed
read DIMM_COUNT IGNORE DIMM_SPEED MHZ < <($DMIDECODE --type 17 | grep Speed: | grep -v Unknown | sort | uniq -c)
# Get cpu bios speed.
CPU_BIOS_SPEED=$($DMIDECODE -s processor-frequency | head -1 | awk '{print $1}')
# Count CPU cores.
CPU_CORE_COUNT=$(grep -c "^processor" /proc/cpuinfo)

# Current usage in /tmp
TMP_USAGE_BYTES=$(du -s /tmp | awk '{print $1}')


  if [[ $IB_PRESENT == "true" ]]; then
    echo "ib_state       = $IB_STATE" 
    echo "ib_link        = $IB_LINK"
    echo "ib_rate        = $IB_RATE" 
    echo "ib_diagssum    = $IB_DIAGSSUM"
  fi
  echo "mem_total      = $MEM_TOTAL" >> $outputpath/$outputfile
  echo "dimm_count     = $DIMM_COUNT" >> $outputpath/$outputfile
  echo "dimm_speed     = $DIMM_SPEED" >> $outputpath/$outputfile
  echo "cpu_bios_speed = $CPU_BIOS_SPEED" >> $outputpath/$outputfile

ERROR="ERROR "

if [[ $IB_PRESENT == "true" ]]; then
  # Check for state error
  if [[ "$IB_STATE" != "$DEFAULT_IB_STATE" ]]; then
    ERROR="${ERROR}IB_STATE_ERROR|"
  fi
  
  # Check for link error
  if [[ "$IB_LINK" != "$DEFAULT_IB_LINK" ]]; then
    ERROR="${ERROR}IB_LINK_ERROR|"
  fi

  # Check for rate error
  echo "ib_rate        = $IB_RATE" >> $outputpath/$outputfile
  echo "ib_rate_def    = $DEFAULT_IB_RATE" >> $outputpath/$outputfile
  if [[ "$IB_RATE" != "$DEFAULT_IB_RATE" ]]; then
    ERROR="${ERROR}IB_RATE_ERROR|"
  fi

  # Check if diag counters are increasing too rapidly.
  DELTA=$(($IB_DIAGSSUM - $LAST_IB_DIAGSSUM))
  THRESHHOLD=16
  IB_DIAG_RATE_EXCEEDED_FILE=/tmp/ib_diag_rate_exceeded
  echo "ib_delta       = $DELTA" >> $outputpath/$outputfile
  echo "ib_delta_def   = $THRESHHOLD" >> $outputpath/$outputfile
  
  if [[ $DELTA -gt $THRESHHOLD || -f $IB_DIAG_RATE_EXCEEDED_FILE ]]; then
    ERROR="${ERROR}IB_DIAGS_ERROR_COUNT_RATE_EXCEEDED|"
    touch $IB_DIAG_RATE_EXCEEDED_FILE
  fi

  # Check if diag counters are over all-time threshhold.
  MAX_ALLOWED_IB_ERRORS=256
  echo "ib_diagsum     = $IB_DIAGSSUM" >> $outputpath/$outputfile
  echo "ib_diagsum_def = $MAX_ALLOWED_IB_ERRORS" >> $outputpath/$outputfile
  if [[ $IB_DIAGSSUM -gt $MAX_ALLOWED_IB_ERRORS ]]; then 
    ERROR="${ERROR}IB_DIAGS_ERROR_COUNT_EXCEEDED|"
  fi

  # Check if ipoib is actually working.
  RETRY=0
  RETRIES=5
  while ! ping -c 1 $IPOIB_PING_TARGET 2>&1 > /dev/null; do
    RETRY=$(( $RETRY + 1 ))
    if [[ $RETRY -gt $RETRIES ]]; then
      ERROR="${ERROR}IP_PING_FAILURE|"
      break
    fi
  done
fi

# Catch case of missing IB card(s) or unexpected IB cards.
if [[ $IB_PRESENT != $DEFAULT_IB_PRESENT ]]; then
  if [[ $DEFAULT_IB_PRESENT == "true" ]]; then
    ERROR="${ERROR}IB_CARD_MISSING|"
  else
    ERROR="${ERROR}IB_CARD_FOUND|"
  fi
fi

# Does this node have a /local/scratch and if so, can we write and delete to it.
if [[ ! -d /local/scratch ]]; then
  ERROR="${ERROR}MISSING_FS_LOCAL_SCRATCH|"
else
  if ( ! touch /local/scratch/health_check || ! rm /local/scratch/health_check ) > /dev/null 2>&1; then
    ERROR="${ERROR}BROKEN_FS_LOCAL_SCRATCH_RO|"
  fi
  if [[ ! -k /local/scratch ]]; then
    ERROR="${ERROR}BROKEN_FS_LOCAL_SCRATCH_PERMS|"
  fi
fi

# Have we seen the OOM fire on this node?
if [[ $(<$OOMFLAG) == "true" ]]; then 
  ERROR="${ERROR}OOM_KILLER|"
  echo "oom            = 0.0" >> $outputpath/$outputfile
else
  echo "oom            = 1.0" >> $outputpath/$outputfile
fi

# Verify total memory is correct.
if [[ "$MEM_TOTAL" != "$DEFAULT_MEM_TOTAL" ]]; then
  ERROR="${ERROR}MEM_TOTAL_ERROR|"
fi
# Verify the number of DIMMs is correct.
if [[ "$DIMM_COUNT" != "$DEFAULT_DIMM_COUNT" ]]; then
  ERROR="${ERROR}DIMM_COUNT_ERROR|"
fi
# Verify Memory is running at proper speed.
if [[ "$DIMM_SPEED" != "$DEFAULT_DIMM_SPEED" ]]; then
  ERROR="${ERROR}DIM_SPEED_ERROR|"
fi
# Verify CPU speed is properly set in bios
if [[ "$CPU_BIOS_SPEED" != "$DEFAULT_CPU_BIOS_SPEED" ]]; then
  ERROR="${ERROR}CPU_BIOS_SPEED_ERROR|"
fi
# Verify CPU core count
if [[ "$CPU_CORE_COUNT" != "$DEFAULT_CPU_CORE_COUNT" ]]; then
  ERROR="${ERROR}CPU_CORE_COUNT_ERROR|"
fi

# Check /tmp for over-full condition.
if [[ "$MAX_TMP_DIR_SIZE" -lt "$TMP_USAGE_BYTES" ]]; then
  ERROR="${ERROR}TMP_DIR_OVER_LIMIT_ERROR|"
fi

# If any errors were encounterd, complain bitterly.
if [[ "$ERROR" != "ERROR " ]]; then
  # Trim trailing |
  ERROR=$(echo ${ERROR}| sed 's/|$//')
  echo "hc             = 0.0" >> $outputpath/$outputfile
  echo $ERROR
  echo "ERROR = " $ERROR >> $outputpath/$outputfile
  #exit 1
else
  echo "hc             = 1.0" >> $outputpath/$outputfile
fi
