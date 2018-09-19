"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import logging
from typing import List

from core import APPLICATION_PROTOCOL, APPLICATION_PORT, APPLICATION_HOST, DATABASE_NAME
from core.elastic.listener import start_listening
from core.v1.search import create_connection
from core.v1.search import init_database


def seed_database(protocol: str = APPLICATION_PROTOCOL, host: str = APPLICATION_HOST, port: int = APPLICATION_PORT,
                  db_name: str = DATABASE_NAME):
    """
    Seeds elastic index with data at (host, port).

    :param protocol: protocol used in to send requests to GraphQl.
    :param host: Host of GraphQl
    :param port: Port to access GraphQl
    :param db_name: Name of discussion-database, could be: discussion
    :return:
    """
    if are_envs_set() or __are_strings_not_empty([protocol, host, port, db_name]):
        logging.debug("Test connection to elastic search is active")
        es = create_connection()
        logging.debug("Connection is established: {0}".format(es.ping()))
        logging.debug("Fill elastic_search database")
        init_database(es, protocol, host, port)
        start_listening()
        logging.debug("Connection is established after seeding: {0}".format(es.ping()))
    else:
        logging.error(
            """(At least) one required environment variables is not set:
                APPLICATION_HOST={0}
                APPLICATION_PORT={1}
                APPLICATION_PROTOCOL={2}
                DATABASE_NAME={3}
            """.format(APPLICATION_HOST, APPLICATION_PORT, APPLICATION_PROTOCOL, DATABASE_NAME))


def are_envs_set() -> bool:
    """
    Checks if the environment variables are set.

    :return:
    """
    return __are_strings_not_empty(APPLICATION_HOST, APPLICATION_PORT, APPLICATION_PROTOCOL, DATABASE_NAME)


def __are_strings_not_empty(*strings: List[str]) -> bool:
    """
    Check if the parameters are set if the environment variables aren't set, because
    the injection doesn't overwrite them.

    :return:
    """
    return "" not in strings


if __name__ == "__main__":
    seed_database()
