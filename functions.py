from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from drip.models import NodeTest
from datetime import datetime, time

def paginator(request, t):
    print len(t)
    paginator = Paginator(t, 5) 
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

def breadcrumb(name=None, year=None, month=None, day=None, hour=None, mi=None):
    
    data = [{'name': 'nodes', 'link': 'nodes'} ]
    if name != None:
        data.append({'name':name, 'link': 'nodes/' + name })
    if year != None:
        data.append({'name': year, 'link': 'nodes/' + name + '/' + year })
    if month != None:
        data.append({'name': month, 'link': 'nodes/' + name + '/' + year +'/' + month })
    if day != None:
        data.append({'name': day, 'link': 'nodes/' + name + '/' + year +'/' + month +'/' + day})
    
    if hour != None and mi == None:
        t = str(time(hour=int(hour)))
        data.append({'name': t, 'link': 'nodes/' + name + '/' + year +'/' + month +'/' + day +'/' + hour  })
        return data
        
    if mi != None:
        t = str(time(hour=int(hour), minute=int(mi)))
        data.append({'name': t, 'link': 'nodes/' + name + '/' + year +'/' + month +'/' + day +'/' + hour +'/' + mi })
    
    return data
    
    
def query(name, year=None, month=None, day=None, hour=None, mi=None):
    
    if year == None:
        return NodeTest.objects.select_related().filter(node_name=name).order_by('-test_date')    
    
    if month == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               test_date__year=year).order_by('-test_date')
    
    if day == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               test_date__year=year, 
               test_date__month=month).order_by('-test_date')
     
    if hour == None:
        return NodeTest.objects.select_related().filter(node_name=name, 
               test_date__year=year, 
               test_date__month=month,
               test_date__day=day).order_by('-test_date')          
    
    if mi == None :
        return NodeTest.objects.select_related().filter(node_name=name, 
               test_date__year=year, 
               test_date__month=month,
               test_date__day=day).order_by('-test_date')    
    
    # Else... do time
    dt = datetime(year=int(year),month=int(month), day=int(day), hour=int(hour), minute=int(mi))
    data = []
    try:
        t2 = NodeTest.objects.select_related().filter(node_name=name, 
               test_date__gt=dt).order_by('-test_date')[0:1].get()
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
