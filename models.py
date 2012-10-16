from django.db import models

class NodeData(models.Model):  
    
    name = models.CharField(max_length=8)
    test_date = models.DateTimeField(db_index=True)
    x1 = models.FloatField(null=True, blank=True)
    x2 = models.FloatField(null=True, blank=True)
    x3 = models.FloatField(null=True, blank=True)
    x4 = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('test_date', 'name')
    
    
   