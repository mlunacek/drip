from django.db import models
from piston.handler import BaseHandler
from piston.utils import rc
from django.db import IntegrityError

class Job(models.Model):
    job_id = models.CharField(max_length=60, unique=True)
    user_name = models.CharField(max_length=60)
    job_name = models.CharField(max_length=60)
    start_time = models.DateTimeField(db_index=True)
    resources = models.CharField(max_length=120,null=True, blank=True)
    test_run = models.BooleanField()

class NodeTest(models.Model):
    job = models.ForeignKey(Job, related_name='job')
    node_name = models.CharField(max_length=8)
    start_time = models.DateTimeField(db_index=True)
        
    def __unicode__(self):
        return self.job.job_id + " " + self.node_name
    
    def test_string(self):
        qs = self.node_test.all().order_by('test_name')
        strlist = [ str(q.value) for q in qs ]
        return ", ".join(strlist)
        
    class Meta:
        unique_together = ('job', 'node_name')
    
class Test(models.Model):
    node_test = models.ForeignKey(NodeTest, related_name='node_test')
    test_name = models.CharField(max_length=60)   
    value = models.FloatField(null=True, blank=True) 
    threshold = models.FloatField(null=True, blank=True) 
    passed = models.NullBooleanField()
    
    def __unicode__(self):
            return self.test_name
    
    class Meta:
        unique_together = ('node_test', 'test_name')

 
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
            

        
                    