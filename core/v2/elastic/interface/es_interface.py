import logging

from core import V2_ST_INDEX
from core.v2.elastic.mapping.mapping import Mapping
from core.v2.elastic.mechanics.es_connector import ESConnector
from core.v2.sql.db_interface.db_interface import DBInterface
from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


class ESInterface(ESConnector, DBInterface):
    """
    This ESInterface combines the ESConnector and the DBInterface to allow the user to work between ES and the DB.

    """

    def __init__(self, index=V2_ST_INDEX, file: str = None):
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
