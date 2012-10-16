
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

'''
# Try this...
r = requests.get('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/1/?format=json')
event = json.loads(r.content)
del event['id']
r = requests.post('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/',
                     data=json.dumps(event),
                     headers={'content-type': 'application/json'})
print r.status_code
print r.raise_for_status()
print r.content                         
print "-----------------------------"                         



r = urllib2.urlopen('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/?format=json')
r.getcode()
d = r.read()

obj = json.loads(d)['objects'][0]
print obj

# post a request
headers = {'content-type': 'application/json'}
r = requests.put('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/1/?format=json', data=json.dumps(obj),headers=headers)
print r.status_code
print r.raise_for_status()
print r.content

# get a request
r = requests.get('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/schema?format=json')
print r.status_code
obj2 = json.loads(r.content)
print obj2['allowed_detail_http_methods']
print obj2['fields']

tmp = {'test1': 488.0, 'test3': 444.0, 'test2': 484.0, 'name': 'node1430', 'test4': 888.0, 'test_date': '2012-10-15T21:15:34', 'id': 1, 'resource_uri': '/benchmarks/api/v1/nodedata/1/'}
tmp = {'test1': 488.0, 'test3': 444.0, 'test2': 484.0, 'name': 'node1430', 'test4': 888.0, 'test_date': '2012-10-15T21:15:34'}

tmp['name'] = 'node1450'
# put a request
headers = {'content-type': 'application/json'}
r = requests.post('http://127.0.0.1:8000/benchmarks/api/v1/nodedata/?format=json', data=json.dumps(obj),headers=headers)
print r.status_code
print r.raise_for_status()

'''




