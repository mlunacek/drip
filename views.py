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

def node_query(request):
    data={}
    form=NodeQueryForm(request.POST or None)
    data["form"]= form
    
    if request.method == 'POST':
        if form.is_valid(): 
            node_name=form.cleaned_data['node_name']
            
            return HttpResponseRedirect("/benchmarks/nodes/" + node_name) 
         
    return render(request,'node_query.html', data)
    

def node_view(request, name):
    
    t = NodeTest.objects.select_related().filter(node_name=name).order_by('-test_date')
    print t
    paginator = Paginator(t, 100) 
    print paginator
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    data = {}
    print objects
    data["node_list"] = objects
         
    return render(request,'node_view.html', data)
    
   
    
def node_detail_view(request, name, node_test_id):
    
    data={}
    t = NodeTest.objects.select_related().filter(id=node_test_id)
    print t
    data["node"] = t
    data["name"] = name

    return render(request,'node_view_detail.html',data)