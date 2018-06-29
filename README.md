# Semantic Search for D-BAS
[![Docker Build Status](https://img.shields.io/docker/build/hhucn/dbas-search.svg)](https://hub.docker.com/r/hhucn/dbas-search/tags/)

This service implements the basic search functions expected by D-BAS.

At the core Search uses [Elasticsearch](https://www.elastic.co/de/).

The latest stable and development image will automatically be deployed to [Docker Hub](https://hub.docker.com/r/hhucn/dbas-search/)

## Preparation
Because this service regards to D-BAS it is necessary to add those parameters used in D-BAS.
Add them to your ***.env**-file (e.g. the development.env).

Those parameters are:

```
DBAS_HOST=web
DBAS_PORT=4284
DBAS_PROTOCOL=http
DB_USER=postgres
DB_NAME=discussion
DB_HOST=db
DB_PW=<secret>
```

D-BAS itself must add those parameters to its ***.env**-file along with:
```
DBAS_PROTOCOL=http
SEARCH_NAME=search
SEARCH_PORT=5000
```


## Build

1. Clone this repository
2. Navigate to the directory where this repository is stored
3. Build the image by running
````
$ docker-compose up --build
````

## Run Search parallel to D-BAS
1. Run D-BAS and make sure that it is alive
2. Run Search by using:
```
$docker-compose up
```

## Run Search as an service of D-BAS
1. Simply run:
```
$ docker-compose up
```

## Missing Parameters
If there are parameters missing Search will let you know which parameter is missing.
An possible message could look like this:
```
search_1  | ERROR:root:One environment variable is not set: 
search_1  |  DBAS_HOST=
search_1  |  DBAS_PORT=4284
search_1  |  DBAS_PROTOCOL=http
```
If you get this message the **index** of Elasticsearch won't be seeded properly.
Also the **listener** for the database won't start till Search got every parameters to run safely.

Till there is a parameter missing it is possible to seed the **index** and start the **listener** by using the following command
from inside the D-BAS container:
```
curl -H "Content-Type: application/json" -X POST -d '{"DBAS_HOST":"web","DBAS_PORT":"4284","DBAS_PROTOCOL":"http"}' http://search:5000/init
``` 
This route is called the init-route. It is only then activated if there is an parameter missing.
After this POST the init route won't be activated any more.

## Routes
If there were no mistakes Search provides several routes for requesting results over the Flask-Server at port 5000.

Those routes look like:
```
GET /suggestions?id=<issue_uid>&position=<position>&search=<search_text>
GET /edits?id=<issue_uid>&statement_uid=<statement_uid>&search=<search_text>
GET /duplicates_reasons?id=<issue_uid>&statement_uid=<statement_uid>&search=<search_text>
GET /statements?id=<issue_uid>&search=<search_text>
POST /init
```

## Results
The response will be a list of dictionaries containing each search result:
```
{
    result:[
        {res1},
        {res2},
        ...
    ]
}
```
Each result (res1, res2, ...) will contain the following information:
```
"html": <highlighted text matching the search results>,
"statement_uid": <uid of statement the text belongs to>,
"text": <textversion of the statement>,
"score": <elastics ranking of the search results>

```

## Index content
If you want to see whats inside the **index** use the following command to display it in your browser:
```
localhost:9200/database/_search?pretty=true&q=*:*&size=1000
```
