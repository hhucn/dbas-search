#!/bin/bash

# Start Flask Server
python3.6 /code/search_service/interface.py &

echo ":: Start elasticsearch"
# Start Elastic-Search
bash /usr/local/bin/docker-entrypoint.sh
