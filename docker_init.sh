#!/bin/bash

echo ":: Start docker_init"

function setup_data {
    echo ":: Setup data and interface"
    python3.6 /code/search_service/create_database.py
    python3.6 /code/search_service/interface.py
}

function wait_for_elastic {
    while ! echo exit | nc 0.0.0.0 9200 > /dev/null 2>&1; do
        echo ":: Waiting for elasticsearch on 0.0.0.0:9200"
        sleep 1;
    done
    echo ":: Elastic launched on 0.0.0.0:9200"

    setup_data &
}

function wait_for_dbas {
    while ! echo exit | nc $DBAS_HOST $DBAS_PORT > /dev/null 2>&1; do
        echo ":: Waiting for D-BAS on ${DBAS_HOST}:${DBAS_PORT}"
        sleep 1;
    done
    echo ":: D-BAS launched on ${DBAS_HOST}:${DBAS_PORT}"
}

wait_for_dbas

wait_for_elastic & disown

python3.6 /code/search_service/elastic/listener.py & disown

echo ":: Start elasticsearch"

bash /usr/local/bin/docker-entrypoint.sh
