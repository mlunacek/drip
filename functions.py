from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from drip.models import Job, NodeTest, Test
from datetime import datetime, time
from django.db.models import Sum


def node_query():
    current = datetime.now()
    sql = 'SELECT t.id, t.node_name, j.job_id, max(j.start_time) as max_start_time FROM drip_nodetest AS t, drip_job AS j '
    sql = sql + 'WHERE j.id = t.job_id AND j.start_time <= "' + str(current) + '" AND j.test_run = 1 ' 
    sql = sql + 'GROUP BY node_name'
    print sql
    test_ids = []
    for p in NodeTest.objects.raw(sql):
        test_ids.append(p.id) 
    
    t = NodeTest.objects.select_related().filter(id__in=test_ids)
    return t
    
def node_snapshot():
    current = datetime.now()
    sql = 'SELECT t.id, t.node_name, j.job_id, max(j.start_time) as max_start_time FROM drip_nodetest AS t, drip_job AS j '
    sql = sql + 'WHERE j.id = t.job_id AND j.start_time <= "' + str(current) + '" AND j.test_run = 1 ' 
    sql = sql + 'GROUP BY node_name'
    print sql
    test_ids = []
    for p in NodeTest.objects.raw(sql):
        test_ids.append(p.id) 
    
    t = NodeTest.objects.select_related().filter(id__in=test_ids).annotate(num_errors=Sum('node_test__passed')).order_by('num_errors')
       
    return t    

def node_snapshot():
    current = datetime.now()
    sql = 'SELECT t.id, t.node_name, j.job_id, max(j.start_time) as max_start_time FROM drip_nodetest AS t, drip_job AS j '
    sql = sql + 'WHERE j.id = t.job_id AND j.start_time <= "' + str(current) + '" AND j.test_run = 1 ' 
    sql = sql + 'GROUP BY node_name'
  
    test_ids = []
    for p in NodeTest.objects.raw(sql):
        test_ids.append(p.id) 
    
    t = NodeTest.objects.select_related().filter(id__in=test_ids)
    return t    

def job_get_username(job_id):
    return "molu8455"

def job_get_user_ids(username):
    jobs = Job.objects.filter(user_name=username).order_by('-start_time')
    return jobs

def job_query_before(st, node_list, job_id):
    
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
    
def job_query_after(st, node_list, job_id):    
            
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

def job_query(job_id):
    
    data = {}
    node_list =[]
    job = Job.objects.select_related().filter(job_id=job_id)[0:1].get()
    for x in job.job.all():
        node_list.append(x.node_name)
    data['job_id'] = job_id
    data['start_time'] = job.start_time
    data['node_list'] = node_list
    
    data['before'] = job_query_before(job.start_time, node_list, job_id)
    data['after'] = job_query_after(job.start_time, node_list, job_id)
    return data



def paginator(request, t):
    print len(t)
    paginator = Paginator(t, 100) 
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    data = {}
    data["node_list"] = objects
    return data

def job_breadcrumb(username=None, job_id=None, node_test_id=None):
    data = [{'name': 'home', 'link': 'benchmarks'} , {'name': 'jobs', 'link': 'benchmarks/jobs'}]
    if username != None:
        data.append({'name':username, 'link': 'benchmarks/jobs/' + username })
    if job_id != None:
        data.append({'name': job_id, 'link': 'benchmarks/jobs/' + username + '/' + job_id })
    if node_test_id != None:
        data.append({'name': node_test_id, 'link': 'benchmarks/jobs/' + username + '/' + job_id + '/' + node_test_id })
    
    return data
    
def breadcrumb(name=None, year=None, month=None, day=None, id=None):
    
    data = [{'name': 'home', 'link': 'benchmarks'} , {'name': 'nodes', 'link': 'benchmarks/nodes'}]
    if name != None:
        data.append({'name':name, 'link': 'benchmarks/nodes/' + name })
    if year != None:
        data.append({'name': year, 'link': 'benchmarks/nodes/' + name + '/' + year })
    if month != None:
        data.append({'name': month, 'link': 'benchmarks/nodes/' + name + '/' + year +'/' + month })
    if day != None:
        data.append({'name': day, 'link': 'benchmarks/nodes/' + name + '/' + year +'/' + month +'/' + day})
            
    if id != None:
        data.append({'name': id, 'link': 'benchmarks/nodes/' + name + '/' + year +'/' + month +'/' + day +'/' + id })
    
    return data
    
    
def query(name, year=None, month=None, day=None, hour=None, mi=None):
    
    if year == None:
        return NodeTest.objects.select_related().filter(node_name=name).order_by('-job__start_time')    
    
    if month == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               job__start_time__year=year).order_by('-job__start_time')
    
    if day == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               job__start_time__year=year, 
               job__start_time__month=month).order_by('-job__start_time')
     
    if hour == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               job__start_time__year=year, 
               job__start_time__month=month,
               job__start_time__day=day).order_by('-job__start_time')          
    
    if mi == None :
        return NodeTest.objects.select_related().filter(node_name=name, 
               job__start_time__year=year, 
               job__start_time__month=month,
               job__start_time__day=day).order_by('-job__start_time')    
    
    # Else... do time
    dt = datetime(year=int(year),month=int(month), day=int(day), hour=int(hour), minute=int(mi))
    data = []
    try:
        t2 = NodeTest.objects.select_related().filter(node_name=name, 
               test_date__gt=dt).order_by('-job__start_time')[0:1].get()
        data.append(t2)
    except:
        pass
    try:
        t1 = NodeTest.objects.select_related().filter(node_name=name, 
               test_date__lte=dt).order_by('-test_date')[0:1].get()
        data.append(t1)       
    except:
        pass    
    
    return data
