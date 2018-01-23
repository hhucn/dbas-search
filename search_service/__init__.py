import os

INDEX_NAME = "database"
DOC_TYPE = "json"

ELASTIC_HOST = os.environ['ELASTIC_HOST']
ELASTIC_PORT = os.environ['ELASTIC_PORT']

DBAS_HOST = os.environ['DBAS_HOST']
DBAS_PORT = os.environ['DBAS_PORT']
DBAS_PROTOCOL = os.getenv('DBAS_PROTOCOL', "http")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
