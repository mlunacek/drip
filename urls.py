from django.conf.urls.defaults import *
from piston.resource import Resource
from drip.models import NodeTestHandler

nodetest_handler = Resource(NodeTestHandler)

urlpatterns = patterns('',
   url(r'^api/node/(?P<emitter_format>.+)/$', nodetest_handler),
)