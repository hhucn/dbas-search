Installation
============

D-BAS-Search works with Docker.

To get D-BAS-Search simply clone the following repository::

    $ git clone https://github.com/hhucn/dbas-search.git

To build an image navigate to search_service run::

    $ docker-compuse up --build

This should build a new image of D-DBAS-Search.

You can see the new image with::

    $ docker images

To run an container simply use::

    $ docker-compose up

To enter an running Container use::

    $ docker exec -it <container name> bash

To stop an running Container use::

    $ docker-compose stop


Environment-Variables
=====================

To launch search in connection with D-BAS it is necessary to set some environment-variables in order
to connect to the D-BAS application and its database.

Database Variables
==================
+----------------------+--------------------------------------------+
| DB_HOST              | The database host of the D-BAS application |
+----------------------+--------------------------------------------+
| DB_NAME              | The Name of the D-BAS database             |
+----------------------+--------------------------------------------+
| DB_PW                | The Password of the D-BAS database         |
+----------------------+--------------------------------------------+
| DB_USER              | The Name of the D-BAS database user        |
+----------------------+--------------------------------------------+

D-BAS Variables
===============
+----------------------+----------------------------------------------+
| DBAS_PORT            | The Port on which the D-BAS app listens at   |
+----------------------+----------------------------------------------+
| DBAS_PROTOCOL        | The Protocol which is used for D-BAS GraphQL |
+----------------------+----------------------------------------------+
| DBAS_HOST            | The application host of D-BAS                |
+----------------------+----------------------------------------------+