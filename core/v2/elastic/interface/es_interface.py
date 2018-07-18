import logging

from core import INDEX_NAME_2
from core.v2.elastic.mapping.mapping import Mapping
from core.v2.elastic.mechanics.es_connector import ESConnector
from core.v2.elastic.queries.es_query import ESQuery
from core.v2.sql.db_interface.db_interface import DBInterface
from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


class ESInterface(ESConnector, DBInterface):
    """
    This ESInterface combines the ESConnector and the DBInterface to allow the user to work between ES and the DB.

    """

    def __init__(self, index=INDEX_NAME_2, file: str = None):
        """
        Construct a ESInterface.

        :param index: The name of the index to work with.
        :param file:  The filename of the sql command that should be used by the DBInterface.
        """
        ESConnector.__init__(self, index=index)
        DBInterface.__init__(self, file=file)

    def initialize_new_index(self):
        """
        This initializes a new index.

        :return:
        """
        if ESConnector.index_exists(self):
            ESConnector.delete_index(self)
        ESConnector.create_index(self)
        logging.info("Index {0} is created ...".format(self.index_name))
        self.fill_index()
        logging.info("Index {0} is filled ...".format(self.index_name))

    def fill_index(self):
        """
        Fills up all data that are queried with the file specified in the constructor and fills them up
        into the index that is specified in the constructor as well.

        :return:
        """
        content_data = DBInterface.query_data_with_sql(self)
        for content in content_data:
            statement = Statement(content)
            author = Author(content)
            issue = Issue(content)
            data = Mapping.data_mapping(statement, author, issue)
            ESConnector.index_element(self, data)

    def get_source_result(self, field: str = "", text: str = "") -> list:
        """
        This method returns filtered results.

        :param field: where should be searched at
        :param text: the text to be searched
        :return: filtered the _source of the ES search result
        """
        results = self.__get_results_of_field(field=field, text=text, filter_path="")

        return [res.get("_source") for res in results.get("hits").get("hits")] if results is not None else []

    def __get_results_of_field(self, field: str = "", text: str = "", filter_path: str = "") -> dict:
        """
        This method can get the ES search result.

        :param field: the field where ES should look at
        :param text: the text to be searched for
        :param filter_path: the field to be contained in the ES result
        :return:
        """
        return self.search_with(query=ESQuery(field=field, text=text, fuzziness=1).sem_query(),
                                filter_path=filter_path)
