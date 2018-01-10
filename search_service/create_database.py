"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
from search_service import INDEX_NAME, DOC_TYPE
from search_service.elastic.search import create_connection
from search_service.elastic.search import init_database
import logging


def seed_database():
    """
    Seeds the database with the datas of D-BAS.

    :return:
    """

    logging.debug(":: Test connection to elastic search is active")
    es = create_connection()
    logging.debug("Connection is established: {0}".format(es.ping()))

    logging.debug(":: Fill elastic_search database")
    init_database(es)
    logging.debug("Connection is established: {0}".format(es.ping()))
    content = es.get(index=INDEX_NAME, doc_type=DOC_TYPE, id=0)
    logging.debug("Content is set: {0}".format(content is not None))


if __name__ == "__main__":
    seed_database()
