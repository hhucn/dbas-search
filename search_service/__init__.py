import os

INDEX_NAME = "database"
DOC_TYPE = "json"

HOST = "0.0.0.0"
API_PORT = 5000
ELASTIC_PORT = 9200

DBAS_HOST = os.environ["DBAS_HOST"]
DBAS_PORT = os.environ["DBAS_PORT"]
DBAS_PROTOCOL = os.getenv("DBAS_PROTOCOL", "http")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
