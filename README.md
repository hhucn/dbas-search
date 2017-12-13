# Semantic Search for D-BAS
docker run --rm --name test -e DBAS_HOST=dbas.cs.uni-duesseldorf.de -e DBAS_PORT=443 -e DBAS_PROTOCOL=https -p 9200:9200 tmp