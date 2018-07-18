from core import INDEX_NAME_2
from core.v1.search import index_new_element, create_connection


class ESConnector:
    """
    This class creates a connection to Elastic and its basic functions.

    """

    def __init__(self, index=INDEX_NAME_2):
        """
        Constructor of ESConnector to a given index.

        :param index: The index the client want to be connected with
        """
        self.es = create_connection()
        self.index_name = index

    def delete_index(self):
        """
        Delete the one index specified in the constructor.

        :return:
        """
        self.es.indices.delete(index=self.index_name)

    def create_index(self):
        """
        Creates one index specified in the constructor.

        :return:
        """
        self.es.indices.create(index=self.index_name)

    def index_exists(self):
        """
        Checks if the specified in the constructor exist.

        :return: True if the index exists, False if not
        """
        return self.es.indices.exists(index=self.index_name)

    def search_with(self, query, filter_path: str = "") -> dict:
        """
        Search in the index specified in the constructor with a given query

        :param filter_path: filter results by field specified in filter_path
        :param query: Search Query
        :return: Results of the query in the index specified in the constructor.
        """
        return self.es.search(index=self.index_name, body=query, filter_path=[filter_path], request_timeout=30)

    def index_element(self, content):
        """
        Index new element to the index specified in the constructor.

        :param content: Content to be indexed, must match the mapping.
        :return:
        """
        index_new_element(es=self.es, content=content, index=self.index_name)
