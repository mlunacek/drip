from django.conf.urls.defaults import *
from piston.resource import Resource
from drip.models import NodeTestHandler
from drip.views import node, node_detail_view, node_query, node_year, node_year_month, node_year_month_day, node_year_month_day_hour, node_year_month_day_time

nodetest_handler = Resource(NodeTestHandler)

urlpatterns = patterns('',
   url(r'^nodes/$', node_query, name="node_query"),
   url(r'^nodes/(?P<name>\w+)/$', node),
   url(r'^nodes/(?P<name>\w+)/detail/(?P<node_test_id>\d+)/$', node_detail_view, name='node_detail_view'),
   
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/$', node_year),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/$', node_year_month),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', node_year_month_day),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/$', node_year_month_day_hour),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<mi>\d{2})/$', node_year_month_day_time),
   
   url(r'^api/node/(?P<emitter_format>.+)/$', nodetest_handler),
)