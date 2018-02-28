#!/bin/bash

# Start Flask Server
python3.6 /code/search_service/interface.py &

echo ":: Start elasticsearch"
bash /usr/local/bin/docker-entrypoint.sh
