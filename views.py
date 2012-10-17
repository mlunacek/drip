from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


def node_view(request):
    data={}

    



    return render_to_response('node_view.html',data, context_instance=RequestContext(request))