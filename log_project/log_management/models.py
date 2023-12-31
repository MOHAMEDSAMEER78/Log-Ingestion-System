from django.db import models
from elasticsearch_dsl import Document, Date, Text
# Create your models here.

class log(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=10)
    message = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    trace_id = models.CharField(max_length=100)
    span_id = models.CharField(max_length=100)
    commit = models.CharField(max_length=100)
    parentResourceId = models.CharField(max_length=100)
    class Meta:
        db_table = 'lis_table'
    def __str__(self):
        return self.level
    
