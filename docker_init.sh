#!/bin/bash

function wait_for_elastic {
    while ! echo exit | nc 0.0.0.0 9200 > /dev/null 2>&1; do
        echo ":: Waiting for elasticsearch on 0.0.0.0:9200"
        sleep 1;
    done
    echo ":: Elastic launched on 0.0.0.0:9200"

    python3.6 /code/search_service/create_database.py &
}

python3.6 /code/search_service/interface.py &

wait_for_elastic & disown

echo ":: Start elasticsearch"
bash /usr/local/bin/docker-entrypoint.sh
