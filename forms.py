from django import forms
from django.template import Context, loader

class NodeQueryForm(forms.Form):
    node_name = forms.CharField(required=True, max_length=8)
    date = forms.CharField(required=False)
    time = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'timepicker-default input-small data-date-format="yyyy-mm-dd"'}))
    
class JobIdForm(forms.Form):
    job_id = forms.CharField(required=False, max_length=60)
    username = forms.CharField(required=False, max_length=60)
    
    def clean(self):
        cleaned_data = super(JobIdForm, self).clean()
        job_id = cleaned_data.get("job_id")
        username = cleaned_data.get("username")
        
        if not job_id and not username:
            raise forms.ValidationError("Please specify either a Username or Job ID")
        
        # Always return the full collection of cleaned data.
        return cleaned_data