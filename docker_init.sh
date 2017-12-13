#!/bin/bash

function lets_go {
    while ! echo exit | nc localhost 9200 > /dev/null 2>&1; do
        sleep 3;
        echo ":: Waiting for elasticsearch to launch on 9200"
    done

    python3.6 /code/search_service/init_elastic_db.py
}

while ! echo exit | nc $DBAS_HOST $DBAS_PORT > /dev/null 2>&1; do
    sleep 3;
    echo ":: Waiting for D-BAS to launch on ${DBAS_HOST}:${DBAS_PORT}"
done

lets_go & disown

echo ":: Start elasticsearch"

bash /usr/local/bin/docker-entrypoint.sh

