import os

V1_DB_INDEX = "database"
STATEMENT_INDEX = "statement"
DOC_TYPE = "json"

APPLICATION_HOST = os.getenv("APPLICATION_HOST", "")
APPLICATION_PORT = os.getenv("APPLICATION_PORT", "")
APPLICATION_PROTOCOL = os.getenv("APPLICATION_PROTOCOL", "http")
DATABASE_NAME = os.getenv("DATABASE_NAME", "discussion")

FILTER = {"en": "synonyms_english", "de": "synonyms_german"}
