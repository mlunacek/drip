from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from drip.models import NodeTest, Test
from drip.forms import NodeQueryForm

from datetime import datetime, time
import functions

def node_query(request):
    data={}
    form=NodeQueryForm(request.POST or None, initial={'node_name': 'node1430', 'date':'2012-10-18', 'time':'11:05 PM'})
    data["form"]= form
    data["breadcrumb"] = functions.breadcrumb()
    t = NodeTest.objects.select_related().filter(node_name='node1430').order_by('-test_date')
    print t
    
    
    if request.method == 'POST':
        if form.is_valid(): 
            node_name=form.cleaned_data['node_name']
            date_str = form.cleaned_data['date']
            time_str = form.cleaned_data['time']
            
            link_str = ["/benchmarks/nodes"]
            link_str.append(node_name)
            print link_str 
            print date_str
            if date_str == "":
                return HttpResponseRedirect("/".join(link_str))     
            
            d_year = date_str[:4]
            d_month = date_str[5:7]
            d_day = date_str[8:10]
            d_hour = time_str[:2]
            d_min = time_str[3:5]
            d_flip = time_str[6:8]
            if d_flip == 'PM':
                d_hour = str(int(d_hour) + 12)
             
            link_str.append(str(d_year))   
            link_str.append(str(d_month))
            link_str.append(str(d_day))   
            link_str.append(str(d_hour))
            link_str.append(str(d_min))    
          
            return HttpResponseRedirect("/".join(link_str)) 
         
    return render(request,'node_query.html', data)

def node_detail_view(request, name, node_test_id):
    data={}
    t = NodeTest.objects.select_related().filter(id=node_test_id)
    print t
    data["node"] = t
    data["breadcrumb"] = functions.breadcrumb(name)
    return render(request,'node_view_detail.html',data)
    
def node(request, name):  
    t = functions.query(name)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name)
    return render(request,'node_view.html', data)

def node_year(request, name, year):
    t = functions.query(name, year)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name,year)
    return render(request,'node_view.html', data)

def node_year_month(request, name, year, month):
    t = functions.query(name, year, month)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name,year,month)
   
    return render(request,'node_view.html', data)

def node_year_month_day(request, name, year, month, day):
    t = functions.query(name, year, month, day)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name,year,month,day)
    return render(request,'node_view.html', data)

def node_year_month_day_hour(request, name, year, month, day, hour):
    t = functions.query(name, year, month, day, hour)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name,year,month, day, hour)
    return render(request,'node_view.html', data)  

def node_year_month_day_time(request, name, year, month, day, hour, mi):
    t = functions.query(name, year, month, day, hour, mi)
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb(name,year,month, day, hour,mi)
    return render(request,'node_view.html', data)  
    

    
    
    
    
    
    
    
    
    
    
    
    