"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import logging

from search_service.elastic.search import create_connection
from search_service.elastic.search import init_database


def seed_database():
    """
    Seeds the database with the datas of D-BAS.

    :return:
    """

    logging.debug("Test connection to elastic search is active")
    es = create_connection()
    logging.debug("Connection is established: {0}".format(es.ping()))

    logging.debug("Fill elastic_search database")
    init_database(es)
    logging.debug("Connection is established after seeding: {0}".format(es.ping()))


if __name__ == "__main__":
    seed_database()
