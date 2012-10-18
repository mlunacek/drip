from django import forms
from django.template import Context, loader

class NodeQueryForm(forms.Form):
    node_name = forms.CharField(required=True, max_length=8)
    
    