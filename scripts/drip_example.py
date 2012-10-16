
import json
import requests

r = requests.get('http://127.0.0.1:8000/benchmarks/api/node/json/')
if r.status_code != 200:
    print r.raise_for_status()


# Here are a few templates
tmp = json.dumps([{
        "test_date": "2012-10-16T13:57:44", 
        "node_name": "node3889",
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
 

