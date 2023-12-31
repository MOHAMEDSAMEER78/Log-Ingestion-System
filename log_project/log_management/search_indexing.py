from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date
from elasticsearch.exceptions import NotFoundError
from .models import log  # Assuming your model is named Log with an uppercase 'L'

# Define an Elasticsearch document for the Log model
class LogIndexNotFoundError(NotFoundError):
    pass
class LogIndex(Document):
    log_id = Text()
    level = Text()
    message = Text()
    resource_id = Text()
    timestamp = Date()
    trace_id = Text()
    span_id = Text()
    commit = Text()
    parentResourceId = Text()

    class Index:
        name = 'log_index'

# Establish connection to Elasticsearch
connections.create_connection(hosts=['https://localhost:9200'])  # Replace with your Elasticsearch server details

# Function to index a Log instance
def index_log(log_instance):
    log_document = LogIndex(
        meta={'id': str(log_instance.id)},  # Convert id to string
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

# Function to update an indexed Log document
def update_document(log_id, log_instance):
    try:
        log_document = LogIndex.get(id=str(log_id))  # Convert id to string
        log_document.update(
            level=log_instance.level,
            message=log_instance.message,
            resource_id=log_instance.resource_id,
            timestamp=log_instance.timestamp,
            trace_id=log_instance.trace_id,
            span_id=log_instance.span_id,
            commit=log_instance.commit,
            parentResourceId=log_instance.parentResourceId
        )
    except NotFoundError:
        pass  
