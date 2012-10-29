from django.conf.urls.defaults import *
from piston.resource import Resource
from drip.models import NodeTestHandler
from drip.views import node_snapshot, job_query, job_username, job_id, job_id_detail, node, node_detail_view, node_query, node_year, node_year_month, node_year_month_day, node_year_month_day_id
nodetest_handler = Resource(NodeTestHandler)

urlpatterns = patterns('',
   
   url(r'^jobs/$', job_query, name="job_query"),
   url(r'^jobs/(?P<username>\w+)/$', job_username, name="job_username"),
   url(r'^jobs/(?P<username>\w+)/(?P<job_id>\w+)/$', job_id, name='job_id'),
   url(r'^jobs/(?P<username>\w+)/(?P<job_id>\w+)/(?P<node_test_id>\d+)/$', job_id_detail, name='job_id_detail'),
   
   url(r'^nodes/$', node_query, name="node_query"),
   url(r'^nodes/snapshot/$', node_snapshot, name='node_snapshot'),
   url(r'^nodes/(?P<name>\w+)/$', node),
   url(r'^nodes/(?P<name>\w+)/detail/(?P<node_test_id>\d+)/$', node_detail_view, name='node_detail_view'),
   
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/$', node_year),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/$', node_year_month),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', node_year_month_day),
   url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<job_id>\w+)/$', node_year_month_day_id),
   #url(r'^nodes/(?P<name>\w+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<mi>\d{2})/$', node_year_month_day_time),
   
   url(r'^api/node/(?P<emitter_format>.+)/$', nodetest_handler),
)