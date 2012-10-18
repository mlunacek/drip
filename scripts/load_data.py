import json
import requests

import os, sys, ConfigParser
from datetime import datetime 
from optparse import OptionParser

appsdir = '/root/srv/www/benchmarks/apps/'
#appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/apps/'
if not appsdir in sys.path:
    sys.path.insert(0,appsdir)
    
appsdir = '/root/srv/www/benchmarks/'
#appsdir = '/Users/mlunacek/Sites/performance/benchmarks_2.0/'
if not appsdir in sys.path:
    sys.path.insert(1,appsdir)    

os.environ["DJANGO_SETTINGS_MODULE"] = "benchmarks_site.settings"
from django.db import models
from drip.models import NodeTest, Test
from django.db import IntegrityError

def crud(nodename):
    r = requests.get('http://127.0.0.1:8000/benchmarks/api/node/json/')
    if r.status_code != 200:
        print r.raise_for_status()


    # Here are a few templates
    tmp = json.dumps([{
        "test_date": "2012-10-16T13:57:44", 
        "node_name": nodename,
        "node_test":[ { "value": 111.0, "test_name": "s1" }, 
                      { "value": 222.0, "test_name": "s2" }, 
                      { "value": 222.0, "test_name": "s3" }, 
                      { "value": 222.0, "test_name": "s4" }, 
                      { "value": 222.0, "test_name": "l1" }, 
                      { "value": 222.0, "test_name": "l2" }
                    ]
                    }])

    r = requests.post('http://127.0.0.1:8000/benchmarks/api/node/json/',
                     data=tmp,
                     headers={'content-type': 'application/json'})
    if r.status_code == 201:
        print r.content   
    elif r.status_code == 409:
        print "Conflict"
    else:
        print r.raise_for_status()

def create_test(config,test_node,section,value):
    
    try:
        xdata = config.getfloat(section, value)
    except ValueError as e:
        xdatatmp = config.getboolean(section, value)
        if xdatatmp:
            xdata = 1.0
        else:
            xdata - 0.0
    print xdata
    
    test_x = Test(test_name=value, value=xdata, node_test=test_node)
    try:
        test_x.save()
    except IntegrityError as e:
        print "Integrity Error"


def direct(input_file):
    
    config = ConfigParser.ConfigParser()
    config.read(input_file)
    
    node_name = config.get('meta', 'node_name')
    date_str = config.get('meta', 'date_string')
    
    d_year = int(date_str[:4])
    d_month = int(date_str[4:6])
    d_day = int(date_str[6:8])
    d_hour = int(date_str[9:11])
    d_min = int(date_str[12:14])
       
    dt = datetime(year=d_year, month=d_month, day=d_day, hour=d_hour, minute=d_min)
    
    # Create the node test 
    test_node_i = NodeTest(node_name=node_name,test_date=dt)
    try:
        test_node_i.save()
    except IntegrityError as e:
	    print "Integrity Error"
    
    create_test(config,test_node_i,'stream','s1')
    create_test(config,test_node_i,'stream','s2')
    create_test(config,test_node_i,'stream','s3')
    create_test(config,test_node_i,'stream','s4')
    create_test(config,test_node_i,'linpack','l1')
    create_test(config,test_node_i,'linpack','l2')
    create_test(config,test_node_i,'meta','omm_passed')
    create_test(config,test_node_i,'meta','health_check_passed')

#==============================================================================  
if __name__ == '__main__':      
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="inputfile")
    (options, args) = parser.parse_args()
    
    # get the options
    if options.file:
    	input_file = options.file
        #crud("node1023")
        direct(input_file)


