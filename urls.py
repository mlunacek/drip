from django.conf.urls.defaults import *
from piston.resource import Resource
from drip.models import NodeTestHandler
from drip.views import node_view, node_detail_view, node_query

nodetest_handler = Resource(NodeTestHandler)

urlpatterns = patterns('',
   url(r'^nodes/$', node_query, name="node_query"),
   url(r'^nodes/(?P<name>\w+)/$', node_view),
   url(r'^nodes/(?P<name>\w+)/(?P<node_test_id>\d+)/$', node_detail_view, name='node_detail_view'),
   url(r'^api/node/(?P<emitter_format>.+)/$', nodetest_handler),
   
   
)