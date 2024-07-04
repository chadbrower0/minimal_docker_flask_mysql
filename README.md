# minimal_docker_flask_mysql
A minimal viable example of using docker-compose to setup flask and mysql for a webapp


## Purpose of this repository 

  Suppose you want to create a simple, web application, using python and a local database.
  You could set up your own web server on a dedicated Linux machine, but the system administration can be a burden.
  You could use a virtual machine to reduce some of that burden and cost, but installing and configuring services is still quite a bit of work.
  Instead, a docker virtual file system can setup the services for you, and it is very resource-efficient.
  Here is an example of how to configure and run docker, flask, and MySQL.


## Explanation of directories and files

 * `databaseData/`	A directory on the host machine that persists database data between docker container instantiations
 * `secrets/`	Files containing database passwords
 * `webserver/`	Code for the flask webserver
   * `Dockerfile`	Docker sub-configuration for the webserver
   * `main.py`	Main python entry point
   * `static`	Files served as-is
   * `templates`	Files served with variable substitutions and other template logic
 * `docker-compose.yml`	The main docker configuration file


## To run:

 * `mkdir database_data`
 * `docker compose up --build`

 
## Explanation of processes
  
  A docker container is created for the database service, and another for the webserver.
  When creating the initial database container, the docker environment variables like `MYSQL_ROOT_PASSWORD_FILE` cause the base mysql image to automatically
  create a database, set the admin password, and set the webserver's database user and password.
  The database network and port are exposed only to the webserver, and the webserver exposes itself to the world.
  The webserver container automatically starts the flask service, which initially creates a database table,
  and then updates the database with each webpage served.


## To do next:

 * Modify the passwords in your `secrets/` files.
 * Modify the python code in `webserver/main.py` to create your database schema, website content, and business logic.
 * If you want the database to be reconfigured from scratch, recreate the database data directory.

    `rm -rf database_data  &&  mkdir database_data`


