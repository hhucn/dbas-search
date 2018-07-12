import os

from core.v2.sql.db_mechanics.dbconnector import DBConnector
from core.v2.sql.sql_commands.sql_adapter import SQLAdapter


class DBInterface(DBConnector, SQLAdapter):
    """
    This class is a interface between the Database and a User.
    It combines the DatabaseConnector class and the SQLAdapter class.
    With this it is possible to combine the functionality of both classes.
    It allows the user to interact and query with the database.
    """

    def __init__(self, host: str = os.environ["DB_HOST"], user: str = os.environ["DB_USER"],
                 name: str = os.environ["DB_NAME"],
                 pw: str = os.environ["DB_PW"], file: str = None):
        """
        This init a instance of DBInterface and it combines the functionality
        of the Database class and the SQLAdapter class.

        :param host: <db-host>
        :param user: <db-user>
        :param name: <db-name>
        :param pw: <db-password>
        :param file: File  where the sql-query is stored.
        """
        DBConnector.__init__(self, host=host, user=user, name=name, pw=pw)
        SQLAdapter.__init__(self, file=file)

    def query_data_with_sql(self) -> list:
        """
        This method queries with the sql-query defined in self.path.

        :return: List of result queried with the sql-file in self.path.
        """
        return DBConnector.query(self, query=SQLAdapter.read_file(self))
