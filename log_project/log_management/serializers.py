from rest_framework import serializers
from .models import log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = log
        fields = ('id', 'level', 'message', 'resource_id', 'timestamp', 'trace_id', 'span_id', 'commit', 'parentResourceId')


