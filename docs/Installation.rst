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
+----------------------+--------------------------------------------------------------------+
| DATABASE_HOST        | The database host used in the  D-BAS application                   |
+----------------------+--------------------------------------------------------------------+
| DATABASE_NAME        | The name of the database used by the D-BAS application             |
+----------------------+--------------------------------------------------------------------+
| DATABASE_PASSWORD    | The password of the database used by the D-BAS application         |
+----------------------+--------------------------------------------------------------------+
| DATABASE_USER        | The name of the database user used by the D-BAS application        |
+----------------------+--------------------------------------------------------------------+

D-BAS Variables
===============
+----------------------+-----------------------------------------------------------------------+
| APPLICATION_PORT     | The Port on which the D-BAS application listens at                    |
+----------------------+-----------------------------------------------------------------------+
| APPLICATION_PROTOCOL | The Protocol which is required by D-BAS to query with GraphQL         |
+----------------------+-----------------------------------------------------------------------+
| APPLICATION_HOST     | The application host of D-BAS                                         |
+----------------------+-----------------------------------------------------------------------+