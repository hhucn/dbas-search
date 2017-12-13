import os

# todo rename address to host
ELASTIC_SEARCH_ADDRESS = "localhost"
ELASTIC_SEARCH_PORT = 9200

DBAS_HOST = os.environ['DBAS_HOST']
DBAS_PORT = os.environ['DBAS_PORT']
DBAS_PROTOCOL = os.getenv('DBAS_PROTOCOL', "http")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
