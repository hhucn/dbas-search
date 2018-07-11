import os

from core.v2.sql.db_mechanics.database import Database
from core.v2.sql.db_mechanics.sql_adapter import SQLAdapter


class DBInterface(Database, SQLAdapter):
    """
    This class is a interface between the Database and a User.
    It combines the Database class and the SQLAdapter class.
    With this it is possible to combine the functionality of both classes.
    It allows the user to interact and query with the database.
    """

    def __init__(self, host: str = os.environ["DB_HOST"], user: str = os.environ["DB_USER"],
                 name: str = os.environ["DB_NAME"],
                 pw: str = os.environ["DB_PW"], path: str = None):
        """
        This init a instance of DBInterface and it combines the functionality
        of the Database class and the SQLAdapter class.

        :param host: <db-host>
        :param user: <db-user>
        :param name: <db-name>
        :param pw: <db-password>
        :param path: Path where the sql-file is stored that contains the sql query to be searched with.
        """
        Database.__init__(self, host=host, user=user, name=name, pw=pw)
        SQLAdapter.__init__(self, path=path)

    def query_data_with_sql(self) -> list:
        """
        This method queries with the sql-query defined in self.path.

        :return: List of result queried with the sql-file in self.path.
        """
        return Database.query(self, query=SQLAdapter.read_file(self))
