"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from search_service import INDEX_NAME, DOC_TYPE
from search_service.elastic.elastic_search import create_connection
from search_service.elastic.elastic_search import init_database

print(":: Test connection to elastic search is active")
es = create_connection()
print("Connection is established: {0}".format(es.ping()))

print(":: Fill elastic_search database")
init_database(es)
print("Connection is established: {0}".format(es.ping()))
content = es.get(index=INDEX_NAME, doc_type=DOC_TYPE, id=0)
print("Content is set: {0}".format(content is not None))
