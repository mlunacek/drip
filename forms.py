from django import forms
from django.template import Context, loader

class NodeQueryForm(forms.Form):
    node_name = forms.CharField(required=True, max_length=8)
    date = forms.CharField(required=False)
    time = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'timepicker-default input-small data-date-format="yyyy-mm-dd"'}))
    
  