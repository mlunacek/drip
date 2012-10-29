import json
import requests

import os, sys, ConfigParser
from datetime import datetime 
from optparse import OptionParser 


appsdir = '/root/srv/www/benchmarks/apps/'
appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/apps/'
if not appsdir in sys.path:
    sys.path.insert(0,appsdir)
    
appsdir = '/root/srv/www/benchmarks/'
appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/'
if not appsdir in sys.path:
    sys.path.insert(1,appsdir)    

os.environ["DJANGO_SETTINGS_MODULE"] = "benchmarks_site.settings"
from django.db import models
from drip.models import Job, NodeTest, Test
from django.db import IntegrityError

def create_test(test_node, label, value, threshold):
    
    print value
    print threshold
    passed = True
    if value < threshold:
        passed = False
    
    print passed    
    test_x = Test(test_name=label, value=value, node_test=test_node, passed=passed)
    try:
        test_x.save()
    except IntegrityError as e:
        print "Integrity Error"
    

def date_string(date_str):
    d_year = int(date_str[:4])
    d_month = int(date_str[4:6])
    d_day = int(date_str[6:8])
    d_hour = int(date_str[9:11])
    d_min = int(date_str[12:14])
       
    dt = datetime(year=d_year, month=d_month, day=d_day, hour=d_hour, minute=d_min)
    return dt
    

def direct(job_id, start_date, node_name, s1=None, s2=None):
    
    sd = date_string(start_date)
    ed = date_string(start_date)
    user_name = "molu8455"
    print job_id
    print node_name
    print sd
    print ed
    runtest = True
    if s1==None and s2==None:
        runtest = False
    
    # Create the Job or get the job if it's already there
    job = Job(job_id=job_id, user_name=user_name, start_time=sd, end_time=ed, test_run=runtest)
    try:
        job.save()
    except IntegrityError as e:
        job = Job.objects.filter(job_id=job_id)[0:1].get()
    
    # Create the node test
    node_test = NodeTest(job=job, node_name=node_name)
    try:
        node_test.save()
    except IntegrityError as e:
        node_test = NodeTest.objects.filter(job=job, node_name=node_name)[0:1].get()
   
    print job.job_id
    print node_test.node_name
    
    if runtest == True:
        create_test(node_test,'stream',s1, 3100)
        create_test(node_test,'linpack',s2, 145)


direct('100', '20121023:10:00:00', 'node0001', s1=2900, s2=140)
direct('100', '20121023:10:00:00', 'node0002', s1=3000, s2=150)
direct('100', '20121023:10:00:00', 'node0003', s1=2000, s2=130)
direct('100', '20121023:10:00:00', 'node0004', s1=3200, s2=160)

direct('101', '20121023:11:00:00', 'node0001', s1=3100, s2=150)
direct('101', '20121023:11:00:00', 'node0002', s1=2900, s2=140)
direct('101', '20121023:11:00:00', 'node0003', s1=3100, s2=150)

direct('102', '20121023:12:00:00', 'node0004', s1=3100, s2=140)
direct('102B', '20121023:12:05:00', 'node0004', s1=3100, s2=150)

direct('103', '20121023:13:00:00', 'node0001')
direct('103', '20121023:13:00:00', 'node0002')
direct('103', '20121023:13:00:00', 'node0003')
direct('103', '20121023:13:00:00', 'node0004')

direct('104', '20121023:13:00:00', 'node0001')
direct('104', '20121023:13:00:00', 'node0002')
direct('104', '20121023:13:00:00', 'node0003')
direct('104', '20121023:13:00:00', 'node0004')

direct('106', '20121023:18:00:00', 'node0001', s1=3106, s2=156)
direct('106', '20121023:18:00:00', 'node0002', s1=3106, s2=156)

direct('107', '20121023:18:00:00', 'node0003', s1=3107, s2=157)
direct('107', '20121023:18:00:00', 'node0004', s1=3107, s2=157)

direct('108', '20121023:19:00:00', 'node0001', s1=3100, s2=150)
direct('108', '20121023:19:00:00', 'node0002', s1=2900, s2=140)
direct('108', '20121023:19:00:00', 'node0003', s1=3100, s2=150)
direct('108', '20121023:19:00:00', 'node0004', s1=3100, s2=150)







