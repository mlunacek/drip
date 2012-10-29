import json
import requests

import os, sys, ConfigParser
from datetime import datetime 
from optparse import OptionParser 

mycwd = os.getcwd()
mycwd = os.path.split(mycwd)[0]
appsdir = os.path.split(mycwd)[0]

#appsdir = '/root/srv/www/benchmarks/apps/'
#appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/apps/'
if not appsdir in sys.path:
    sys.path.insert(0,appsdir)

appsdir = os.path.split(appsdir)[0]
    
#appsdir = '/root/srv/www/benchmarks/'
#appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/'
if not appsdir in sys.path:
    sys.path.insert(1,appsdir)    

os.environ["DJANGO_SETTINGS_MODULE"] = "benchmarks_site.settings"
from django.db import models
from drip.models import Job, NodeTest, Test
from django.db import IntegrityError

def create_test(config,test_node,section,name,threshold):
    
    try:
        xdata = config.getfloat(section, name)
        passed = True
        if xdata < threshold:
            passed = False
            
        test_x = Test(test_name=name, value=xdata, node_test=test_node, threshold=threshold, passed=passed)
        try:
            test_x.save()
        except IntegrityError as e:
            pass

    except ConfigParser.NoOptionError:
        print "no options"
    except ConfigParser.NoSectionError:
        print "no sections"            

def date_string(date_str):
    d_year = int(date_str[:4])
    d_month = int(date_str[4:6])
    d_day = int(date_str[6:8])
    d_hour = int(date_str[9:11])
    d_min = int(date_str[12:14])
       
    dt = datetime(year=d_year, month=d_month, day=d_day, hour=d_hour, minute=d_min)
    return dt
    
def create_or_get_job(config):
    # Job info
    job_id_tmp = config.get('pbs', 'job_id')
    job_id = job_id_tmp.split('.')[0]
    user_name = config.get('pbs', 'job_user')
    job_name = config.get('pbs', 'job_name')[:60]
    start_date = config.get('script', 'date')    
    sd = date_string(start_date)
    
    print job_id
    print job_name
    print user_name
    print sd
    
    testrun = True
    try:
        name = config.get('Benchmarks', 'name')
    except ConfigParser.NoSectionError:    
        print "no section"
        testrun = False
    
    # Create the Job or get the job if it's already there
    job = Job(job_id=job_id, user_name=user_name, job_name=job_name, start_time=sd, test_run=testrun)
    try:
        job.save()
    except IntegrityError as e:
        job = Job.objects.filter(job_id=job_id)[0:1].get()
    
    script_type = config.get('script', 'type')
    print script_type
    if script_type == 'epilogue':
        resources = config.get('pbs', 'job_resources') 
        job.resources = resources
        job.save()
    
    return job        
    
def create_or_get_node_test(config, job):
    
    try:
        node_name = config.get('health', 'node_name')
        start_date = config.get('script', 'date') 
        sd = date_string(start_date)
    
        # Create the node test
        node_test = NodeTest(job=job, node_name=node_name, start_time=sd)
        try:
            node_test.save()
        except IntegrityError as e:
            node_test = NodeTest.objects.filter(job=job, node_name=node_name)[0:1].get()   

    except ConfigParser.NoOptionError:
        return None
    except ConfigParser.NoSectionError:
        return None    
    
    return node_test     

def direct(input_file):
    
    config = ConfigParser.ConfigParser()
    config.read(input_file)
    
    # Job info
    job = create_or_get_job(config)

    # Node Test
    node_test = create_or_get_node_test(config, job)
    
    print job.job_id    
    if node_test:
        
        print node_test.node_name
    
        create_test(config,node_test,'Benchmarks','stream_copy', 23000)
        create_test(config,node_test,'Benchmarks','stream_scale', 36000)
        create_test(config,node_test,'Benchmarks','stream_add', 36000)
        create_test(config,node_test,'Benchmarks','stream_trial', 37000)
        create_test(config,node_test,'Benchmarks','linpack_5k', 90)
        create_test(config,node_test,'Benchmarks','linpack_10k', 100)
        create_test(config,node_test,'health','oom', 0.5)
        create_test(config,node_test,'health','hc', 0.5)


#==============================================================================  
if __name__ == '__main__':      
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="inputfile")
    (options, args) = parser.parse_args()
    
    # get the options
    if options.file:
    	input_file = options.file
        direct(input_file)


