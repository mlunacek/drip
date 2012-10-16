from django.db import models
from piston.handler import BaseHandler
from piston.utils import rc
from django.db import IntegrityError

TEST_CHOICES = (
    ('s1', 'stream1'),
    ('s2', 'stream2'),
    ('s3', 'stream3'),
    ('s4', 'stream4'),
    ('l1', 'linpack1'),
    ('l2', 'linpack2'),
)    

class NodeTest(models.Model):
    node_name = models.CharField(max_length=8)
    test_date = models.DateTimeField(db_index=True)
    
    def __unicode__(self):
            return self.node_name
    
    class Meta:
        unique_together = ('node_name', 'test_date')
    
class Test(models.Model):
    test_name = models.CharField(max_length=2, choices=TEST_CHOICES)   
    value = models.FloatField(null=True, blank=True) 
    node_test = models.ForeignKey('drip.NodeTest', related_name='node_test')
    
    def __unicode__(self):
            return self.test_name
      
      
            
class NodeTestHandler(BaseHandler):
   
   allowed_methods = ('GET','PUT','POST',)
   fields = ('node_name','test_date', ('node_test', ('test_name', 'value',),),)    
   model = NodeTest
   
   def read(self, name=None):
       return self.model.objects.all()
   
   def create(self, request):
      if request.content_type:
          data = request.data

          for i in data:
                          
              test_node_i = NodeTest(node_name=i['node_name'],test_date=i['test_date'])
              try:
                  test_node_i.save()
              except IntegrityError as e:
                  return rc.DUPLICATE_ENTRY
                        
              for x in i['node_test']:
                  test_x = Test(test_name=x['test_name'], value=x['value'], node_test=test_node_i)
                  try:
                      test_x.save()
                  except IntegrityError as e:
                      return rc.DUPLICATE_ENTRY
   
          return rc.CREATED
      else:
           super(NodeTest, self).create(request)
            

        
                    