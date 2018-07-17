import os

INDEX_NAME = "database"
INDEX_NAME_2 = "statement"
DOC_TYPE = "json"

DBAS_HOST = os.getenv("DBAS_HOST", "")
DBAS_PORT = os.getenv("DBAS_PORT", "")
DBAS_PROTOCOL = os.getenv("DBAS_PROTOCOL", "http")
DB_NAME = os.getenv("DB_NAME", "discussion")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
