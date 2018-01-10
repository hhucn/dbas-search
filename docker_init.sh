#!/bin/bash

echo ":: Start docker_init"

function lets_go {
    while ! echo exit | nc localhost 9200 > /dev/null 2>&1; do
        echo ":: Waiting for elasticsearch to launch on 9200"
        sleep 1;
    done

    python3.6 /code/search_service/create_database.py
}

while ! echo exit | nc $DBAS_HOST $DBAS_PORT > /dev/null 2>&1; do
    echo ":: Waiting for D-BAS to launch on ${DBAS_HOST}:${DBAS_PORT}"
    sleep 1;
done

echo ":: D-BAS launched on ${DBAS_HOST}:${DBAS_PORT}"

lets_go & disown

echo ":: Start elasticsearch"

bash /usr/local/bin/docker-entrypoint.sh

