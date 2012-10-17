from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from drip.models import NodeTest, Test



def node_view(request):
    
    data={}
    
    t = NodeTest.objects.select_related().all()[0]
    print t.id
    print dir(t)
    print t.node_name
    print t.test_date
    d = Test.objects.select_related().filter(node_test=t)
    for x in d:
        print x.test_name + " " + str(x.value) + " " 

    t = NodeTest.objects.select_related().all()[0]
    print t.node_test.all()




    return render_to_response('node_view.html',data, context_instance=RequestContext(request))