from django.conf.urls.defaults import *
from piston.resource import Resource
from drip.handlers import NodeDataHandler

nodedata_handler = Resource(NodeDataHandler)

urlpatterns = patterns('',
   url(r'^api/(?P<emitter_format>.+)/$', nodedata_handler),
)