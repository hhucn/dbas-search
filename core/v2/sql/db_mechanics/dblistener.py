import json
import time
from threading import Thread

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.v2.sql.db_mechanics.dbconnector import DBConnector


class DBListener(Thread):
    """
    This class is a database listener.
    It can listen to specific database event.
    """

    def __init__(self, command: str = "", event: str = "", refresh_time: int = 1, work=None,
                 args: list = []):
        Thread.__init__(self)
        self.command = command
        self.event = event
        self.db_client = DBConnector()
        self.refresh_time = refresh_time
        self.work = work
        self.args = args

    def run(self):
        """
        Listen to a specific database event.

        :return:
        """
        self.db_client.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.db_client.curs.execute(self.command)
        while True:
            self.db_client.conn.poll()
            time.sleep(self.refresh_time)

            while self.db_client.conn.notifies:
                notification = self.db_client.conn.notifies.pop(0)
                payload = json.loads(notification.payload)
                if payload["event"] == self.event:
                    print("Index....")
                    self.work(*self.args)
                    print("Finish....")
