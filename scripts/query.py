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
from django.db.models import Max

def get_node_list(job_id):
    node_list =[]
    job = Job.objects.select_related().filter(job_id=job_id)[0:1].get()
    for x in job.job.all():
        node_list.append(x.node_name)
    return node_list
    
def get_start_time(job_id):
    job = Job.objects.filter(job_id=job_id)[0:1].get()
    return job.start_time

def get_job_information(job_id):
    data = {}
    node_list =[]
    job = Job.objects.select_related().filter(job_id=job_id)[0:1].get()
    for x in job.job.all():
        node_list.append(x.node_name)
    data['job_id'] = job_id
    data['start_time'] = job.start_time
    data['node_list'] = node_list
    return data

def get_node_tests_before_job(st, node_list, job_id):
    
    sql = 'SELECT t.id, t.node_name, j.job_id, max(j.start_time) as max_start_time FROM drip_nodetest AS t, drip_job AS j '
    sql = sql + 'WHERE j.id = t.job_id AND j.start_time <= "' + str(st) + '" AND j.test_run = 1 AND t.node_name in ('  
    sql = sql + "'" + node_list[0] + "'"
    for l in node_list[1:]:
        sql = sql + ", '" + l + "'"
    sql = sql + ") "    
    sql = sql + 'GROUP BY node_name'
    
    test_ids = []
    for p in NodeTest.objects.raw(sql):
        test_ids.append(p.id) 
    
    t = NodeTest.objects.select_related().filter(id__in=test_ids)
    
    return t
    
def get_node_tests_after_job(st, node_list, job_id):    
            
    sql = 'SELECT t.id, t.node_name, j.job_id, min(j.start_time) as min_start_time FROM drip_nodetest AS t, drip_job AS j '
    sql = sql + 'WHERE j.id = t.job_id AND j.start_time > "' + str(st) + '" AND j.test_run = 1 AND t.node_name in ('  
    sql = sql + "'" + node_list[0] + "'"
    for l in node_list[1:]:
        sql = sql + ", '" + l + "'"
    sql = sql + ") "    
    sql = sql + 'GROUP BY node_name'
    
    test_ids = []
    for p in NodeTest.objects.raw(sql):
        test_ids.append(p.id) 
    
    t = NodeTest.objects.select_related().filter(id__in=test_ids)
    
    return t
    
data = get_job_information(sys.argv[1])

before = get_node_tests_before_job(data['start_time'], data['node_list'], data['job_id'])
after = get_node_tests_after_job(data['start_time'], data['node_list'], data['job_id'])

print " before "
for x in before:
    print x.node_name
    for y in x.node_test.all():
        print "      " + y.test_name

print " after "
for x in after:
    print x.node_name
    for y in x.node_test.all():
        print "      " + y.test_name



'''
# What are the test for a job_id
job_id = "1468043.moab.rc.colorado.edu"
t = Test.objects.select_related().filter(node_test__job__job_id=job_id)
for x in t:
    cmd = x.node_test.job.job_id[0:6] + " " + str(x.node_test.job.start_time) + " " + x.node_test.node_name + " " + x.test_name + " " + str(x.value)
    print cmd
print " "


job_id = "1468040.moab.rc.colorado.edu"
t = NodeTest.objects.select_related().filter(job__job_id=job_id)
for x in t:
    cmd = x.job.job_id + " " + str(x.job.start_time) + " " + x.node_name 
    print cmd
    node_name = x.node_name
    test = Test.objects.select_related().filter(node_test__node_name=node_name)
    for b in test:
        print b.test_name + " " + str(b.node_test.job.start_time)
  
  
node_list = ['node1566', 'node1567']    
t = Job.objects.select_related().filter(job__node_name__in=node_list)
for x in t:
    print x.job_id[0:7] + " " + str(x.start_time)
    for y in x.job.all():
        print y.node_name
        #for z in y.node_test.all():
        #    print z.test_name
    print " "

t = NodeTest.objects.filter(node_name__in=node_list).select_related()
for x in t:
    print x.node_name
    print x.job.start_time
    print " "
'''  


'''
node_name = "node1567"
job_id = "1468043.moab.rc.colorado.edu"
t = Test.objects.select_related().filter(node_test__node_name=node_name, node_test__job__job_id=job_id)

for x in t:
    print x.node_test.job.job_id
    print x.node_test.job.start_time
    print x.node_test.node_name
    print x.test_name
    print x.value

'''

