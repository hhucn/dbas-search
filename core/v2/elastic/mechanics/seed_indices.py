from core import STATEMENT_INDEX
from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.sql.db_mechanics.dblistener import DBListener

if __name__ == "__main__":
    ESInterface(file="request.sql").initialize_new_index()

    es_client = ESInterface(index="update", file="request.sql")
    listener = DBListener(command="LISTEN textversions_changes;", event="insert_textversions",
                          work=es_client.reindex_to, args=[STATEMENT_INDEX])
    listener.start()
    listener.join()
