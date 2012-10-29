from drip.models import Job, NodeTest, Test
from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'user_name', 'job_name', 'start_time')
    date_hierarchy  = 'start_time'
    
admin.site.register(Job, JobAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'value', 'node_test','passed')
    
admin.site.register(Test, TestAdmin)

class NodeTestAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'start_time', 'test_string')
    
admin.site.register(NodeTest, NodeTestAdmin)    