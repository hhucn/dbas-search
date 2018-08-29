from core import STATEMENT_INDEX
from core.v2.elastic.interface.es_interface import ESInterface
from core.v2.sql.db_mechanics.dblistener import DBListener

if __name__ == "__main__":
    ESInterface(file="request.sql").initialize_new_index()

    listener_1 = DBListener(index=STATEMENT_INDEX, commands=["LISTEN statements_changes;",
                                                             "LISTEN textversions_changes;",
                                                             "LISTEN issues_changes;",
                                                             "LISTEN users_changes;"])
    listener_1.start()
    listener_1.join()
