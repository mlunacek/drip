from drip.models import NodeTest, Test
from django.contrib import admin

class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'value', 'node_test')
    
admin.site.register(Test, TestAdmin)

class NodeTestAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'test_date')
    
admin.site.register(NodeTest, NodeTestAdmin)    