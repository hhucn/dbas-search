import os

INDEX_NAME = "database"
DOC_TYPE = "json"

DBAS_HOST = os.getenv("DBAS_HOST", "")
DBAS_PORT = os.getenv("DBAS_PORT", "")
DBAS_PROTOCOL = os.getenv("DBAS_PROTOCOL", "http")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
