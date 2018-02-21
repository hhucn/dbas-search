import json
import threading
import time

import psycopg2


def listen_to_db():
    conn = psycopg2.connect(user="postgres", password="DXxCNtfnt!MOo!f8LY1!P%sw3KGzt@s!",
                            database='discussion', host="db")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN textversions_changes;")
    print("Waiting for notifications on channel 'textversions_changes'")
    while 1:
        conn.poll()
        time.sleep(1)
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print("Got NOTIFY:", notify.pid, notify.channel)
            notification = json.loads(notify.payload)
            print(json.dumps(notification, indent=2))


t1 = threading.Thread(target=listen_to_db())
t1.start()
t1.join()
