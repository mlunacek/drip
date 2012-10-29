#!/bin/bash
. /curc/tools/utils/dkinit
use .openmpi-1.4.5_intel-12.1.2
reuse Benchmarks

# What is the load average?
# ------------------------------------------------------------------------

read LOAD < /proc/loadavg
#echo "load = " $LOAD >> /tmp/diagnose/results

# Any other Users on the node?
# -2 for root and USER
# ------------------------------------------------------------------------
NUM_USERS=`ps au | cut -d' ' -f1 | sort | uniq | wc -l`
NUM_USERS=$(($NUM_USERS-2))
#echo "num_users = " $NUM_USERS >> /tmp/diagnose/results

# Stream
# ------------------------------------------------------------------------
#VAR='Copy: 26872.1392 0.3050 0.3049 0.3052 Scale: 40372.5896 0.2032 0.2029 0.2036 Add: 42153.4988 0.2918 0.2915 0.2920 Triad: 42406.5162 0.2901 0.2898 0.2905'
VAR=`stream | grep -A 3 Copy`

COPY=`echo $VAR | awk '{ print $2 }' | awk -F. '{ print $1 }'`
SCALE=`echo $VAR | awk '{ print $7 }' | awk -F. '{ print $1 }'`
ADD=`echo $VAR | awk '{ print $12 }' | awk -F. '{ print $1 }'`
TRIAD=`echo $VAR | awk '{ print $17 }' | awk -F. '{ print $1 }'`

echo "" >> /tmp/diagnose/results
echo "[Benchmarks]" >> /tmp/diagnose/results
echo "name           = $0" >> /tmp/diagnose/results
echo "stream_copy    = " $COPY >> /tmp/diagnose/results
echo "stream_scale   = " $SCALE >> /tmp/diagnose/results
echo "stream_add     = " $ADD >> /tmp/diagnose/results
echo "stream_trial   = " $TRIAD >> /tmp/diagnose/results

# Linpack
# ------------------------------------------------------------------------
WORKDIR=$PBS_O_WORKDIR/$HOSTNAME
mkdir -p $WORKDIR
rm -rf $WORKDIR/linpack_input

cat >> $WORKDIR/linpack_input << EOF
Sample Intel(R) Optimized LINPACK Benchmark data file (lininput_xeon64)
Intel(R) Optimized LINPACK Benchmark data
4                     # number of tests
1000 2000 5000 10000 20000 25000# problem sizes
1000 2000 5000 10000 20000 25000 # leading dimensions
2 2 2 1 1 1  # times to run a test
4 4 4 4 4 4  # alignment values (in KBytes)
EOF


#VAR='Performance Summary (GFlops) Size LDA Align. Average Maximal 1000 1000 4 67.9979 68.9299 2000 2000 4 88.2979 88.3846 5000 5000 4 107.6497 107.6989 10000 10000 4 114.9367 114.9367 End of tests'
VAR=`xlinpack_xeon64 $WORKDIR/linpack_input | grep -A 9 Performance`

rm -rf $WORKDIR

V1=`echo $VAR | awk '{ print $23 }' | awk -F. '{ print $1 }'`
V2=`echo $VAR | awk '{ print $28 }' | awk -F. '{ print $1 }'`

echo "linpack_5k     = " $V1 >> /tmp/diagnose/results
echo "linpack_10k    = " $V2 >> /tmp/diagnose/results




