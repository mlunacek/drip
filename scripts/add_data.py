
import json
import requests
print "-----------------------------"                       
# get a request
r = requests.get('http://127.0.0.1:8000/benchmarks/api/json/')
print r.status_code
print r.content
#print json.loads(r.content)

tmp = json.dumps({
        "test1": 488.0, 
        "test3": 444.0, 
        "test2": 484.0, 
        "name": "node1450", 
        "test_date": "2012-10-15T21:15:34", 
        "test4": 888.0
    })
    
print tmp    

r = requests.post('http://127.0.0.1:8000/benchmarks/api/json/',
                     data=tmp,
                     headers={'content-type': 'application/json'})
print r.status_code
print r.raise_for_status()
print r.content    
