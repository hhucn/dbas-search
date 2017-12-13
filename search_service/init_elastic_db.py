from search_service.elastic.elastic_search import create_elastic_search_client
from search_service.elastic.elastic_search import create_elastic_search_connection

print(":: Test connection to elastic search is active")
es = create_elastic_search_client()
print("Connection is established: {0}".format(es.ping()))


print(":: Fill elasticsearch database")
es = create_elastic_search_connection()
print("Connection is established: {0}".format(es.ping()))
content = es.get(index="test_index", doc_type="json", id=0)
print("Content is set: {0}".format(content is not None))

