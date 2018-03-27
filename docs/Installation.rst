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
