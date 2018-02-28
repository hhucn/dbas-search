"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import logging
import os

from search_service import DBAS_PROTOCOL, DBAS_PORT, DBAS_HOST
from search_service.elastic.search import create_connection
from search_service.elastic.search import init_database


def seed_database(protocol=DBAS_PROTOCOL, host=DBAS_HOST, port=DBAS_PORT):
    """
    Seeds the database with the datas of D-BAS.
    :return:
    """
    if check_if_env_is_set():
        logging.debug("Test connection to elastic search is active")
        es = create_connection()
        logging.debug("Connection is established: {0}".format(es.ping()))
        logging.debug("Fill elastic_search database")
        init_database(es, protocol, host, port)
        logging.debug("Connection is established after seeding: {0}".format(es.ping()))
    else:
        host = os.getenv("DBAS_HOST", "")
        port = os.getenv("DBAS_PORT", "")
        protocol = os.getenv("DBAS_PROTOCOL", "")
        logging.error("One environment variable is not set: \n DBAS_HOST={0}\n DBAS_PORT={1}\n DBAS_PROTOCOL={2}"
                      .format(host, port, protocol))


def check_if_env_is_set():
    host = os.getenv("DBAS_HOST", "")
    port = os.getenv("DBAS_PORT", "")
    protocol = os.getenv("DBAS_PROTOCOL", "")
    return "" not in [host, port, protocol]
