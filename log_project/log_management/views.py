from rest_framework.views import APIView
from rest_framework.response import Response
from .search_indexing import LogIndex
from rest_framework import status
from .serializers import LogSerializer
from .models import log
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from django.db import transaction 
from elasticsearch_dsl.connections import connections
from .search_indexing import LogIndex
from elasticsearch.exceptions import NotFoundError
import ssl

# -------------------------------------------------------------------------------------------------------------
# Elastic search connection
ELASTIC_PASSWORD = "TqVxyAVxcrzEDfwiC12S"
CERT_FINGERPRINT = "78:02:46:81:0B:3F:20:82:F9:FD:F9:9D:DB:2B:50:00:1C:BE:12:83:3B:15:17:34:56:F9:0F:B9:3A:01:C9:AF"
client = Elasticsearch(
    hosts=["https://localhost:9200/"],  # Elasticsearch server address
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    ssl_version=ssl.PROTOCOL_TLSv1_2,
    client_cert="lis_proj/elasticsearch-8.11.1/config/cert.pem",
    client_key="lis_proj/elasticsearch-8.11.1/config/key.pem",
    ca_certs="lis_proj/elasticsearch-8.11.1/config/certs/http_ca.crt",
    http_auth=("elastic", ELASTIC_PASSWORD)
)

client.info()
connections.create_connection(
    alias="default",
    hosts=["https://localhost:9200/"],  # Elasticsearch server address
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    ssl_version=ssl.PROTOCOL_TLSv1_2,
    http_auth=("elastic", ELASTIC_PASSWORD)
)

# -------------------------------------------------------------------------------------------------------------

def home(request):  # Adjusted to accept a request parameter
    return HttpResponse("Hello, this is the Log ingestion page!")

class LogList(APIView):    
    def get(self, request, format=None):  # Adjusted to accept a request parameter
        logs = log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

class InsertLog(APIView):
    def post(self, request):
        data = {
            'level': request.data.get('level'),
            'message': request.data.get('message'),
            'resource_id': request.data.get('resource_id'),
            'trace_id': request.data.get('trace_id'),
            'span_id': request.data.get('span_id'),
            'commit': request.data.get('commit'),
            'parentResourceId': request.data.get('parentResourceId')
        }
        serializer = LogSerializer(data=data)

        if serializer.is_valid():
            with transaction.atomic():
                log_instance = serializer.save()

                log_document = LogIndex(
                    meta={'id': log_instance.id},
                    level=log_instance.level,
                    message=log_instance.message,
                    resource_id=log_instance.resource_id,
                    timestamp=log_instance.timestamp,
                    trace_id=log_instance.trace_id,
                    span_id=log_instance.span_id,
                    commit=log_instance.commit,
                    parentResourceId=log_instance.parentResourceId
                )
                log_document.save()

                return Response("Successfully inserted log", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchLog(APIView):
    def get(self, request, log_id, format=None):
        try:
            log_document = LogIndex.get(id=log_id)
            log_data = {
                'level': log_document.level,
                'message': log_document.message,
                'resource_id': log_document.resource_id,
                'timestamp': log_document.timestamp,
                'trace_id': log_document.trace_id,
                'span_id': log_document.span_id,
                'commit': log_document.commit,
                'parentResourceId': log_document.parentResourceId
            }
            return Response(log_data)
        except NotFoundError:
            return HttpResponse("Log document not found!", status=404)
