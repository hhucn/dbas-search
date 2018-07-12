import os

import psycopg2
from psycopg2.extras import RealDictCursor


class DBConnector:
    """
    This class creates a database connection to the postgresql database.
    It can query data from it.
    But it does not close the database connection and the cursor by it self.

    """

    def __init__(self, host: str = os.environ["DB_HOST"], user: str = os.environ["DB_USER"],
                 name: str = os.environ["DB_NAME"],
                 pw: str = os.environ["DB_PW"]):
        """
        Creates a cursor and a database connection to a database specified by the parameters.

        :param host: <db-host>
        :param user: <db-user>
        :param name: <db-name>
        :param pw: <db-password>
        """
        self.host = host
        self.user = user
        self.name = name
        self.pw = pw
        self.conn = psycopg2.connect(user=self.user, password=self.pw,
                                     database=self.name, host=self.host)
        self.curs = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query: str) -> list:
        """
        With this method it is possible to query data from the database by a own specified SQL-query.

        :param query: sql-query which should be used
        :return: list of results for the query.
        """
        self.curs.execute(query)
        return self.curs.fetchall()

    def close_all(self):
        """
        This will close the existing connection and cursor.

        :return:
        """
        self.conn.close()
        self.curs.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Destructor for the database connection and the cursor.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.close_all()
