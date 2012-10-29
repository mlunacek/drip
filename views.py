from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from drip.models import Job, NodeTest, Test
from drip.forms import NodeQueryForm, JobIdForm

from datetime import datetime, time
import functions

''' Job Views '''

def job_query(request):
    data={}
    form_job=JobIdForm(request.POST or None, initial={'username': 'molu8455'})
    data["form_job"]= form_job
    data["breadcrumb"] = functions.job_breadcrumb()
   
    if request.method == 'POST':
        
        if form_job.is_valid(): 
            if form_job.cleaned_data['username']:  
                username = form_job.cleaned_data['username']
                link_str = ["/benchmarks/jobs/" + username ]
                
            if form_job.cleaned_data['job_id']:
                job_id=form_job.cleaned_data['job_id']
                username = functions.job_get_username(job_id)
                link_str = ["/benchmarks/jobs/" + username ]
                link_str.append(job_id)

            return HttpResponseRedirect("/".join(link_str))
         
    return render(request,'job_query.html', data)

def job_username(request, username):  
    data = {}
    data['username'] = username
    data['job_list'] = functions.job_get_user_ids(username);
    data["breadcrumb"] = functions.job_breadcrumb(username)
    return render(request,'job_username_page.html', data)

def job_id(request, username, job_id):  
    data = functions.job_query(job_id)
    data['username'] = username
    data['job_id'] = job_id
    data["breadcrumb"] = functions.job_breadcrumb(username, job_id)
    return render(request,'job_id_page.html', data)

def job_id_detail(request, username, job_id, node_test_id):
    data = {}
    data["node"]  = NodeTest.objects.select_related().filter(id=node_test_id)
    data["breadcrumb"] = functions.job_breadcrumb(username, job_id, node_test_id)
    
    return render(request,'node_view_detail.html', data)    


''' Node Views'''


def node_query(request):
    data={}
    form_node=NodeQueryForm(request.POST or None, initial={'username': 'molu8455'})
    data["form_node"]= form_node
    data["breadcrumb"] = functions.breadcrumb()
   
    if request.method == 'POST':
        if form_node.is_valid(): 
            node_name=form_node.cleaned_data['node_name']
            link_str = ["/benchmarks/nodes"]
            link_str.append(node_name)
            date_str = form_node.cleaned_data['date']
            if date_str == "":
                return HttpResponseRedirect("/".join(link_str))     
            d_year = date_str[:4]
            d_month = date_str[5:7]
            d_day = date_str[8:10]
            link_str.append(str(d_year))   
            link_str.append(str(d_month))
            link_str.append(str(d_day))
                
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

def node_year_month_day_id(request, name, year, month, day, job_id):
    data={}
    t = NodeTest.objects.select_related().filter(id=job_id)
    print t
    data["node"] = t
    data["breadcrumb"] = functions.breadcrumb(name, year, month, day, job_id)
    return render(request,'node_view_detail.html',data)
    

def node_snapshot(request):
    t = functions.node_snapshot()
    data = functions.paginator(request, t)
    data["breadcrumb"] = functions.breadcrumb('snapshot')
    return render(request,'node_view.html', data)
    
    
    
    
    
    
    
    
    
    
    
    