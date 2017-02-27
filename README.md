# Project451
To start application:

#### Usage
Install dependencies:

* You will need some system packages, so install corresponding packages in your system, like for Ubuntu:

		sudo apt-get install python3 python3-pip postgresql-server-dev-all

* Then install required python3 packages:

		pip3 install -r requirements.txt


Set environment variables:

    export HOST="<Host address>" # otherwise it will use localhost
    export PORT="<Port on which app will be deployed>" # otherwise it will use 5000
    export DATABASE_URI="<sql>://<username>:<password>@<host>:<port>/<database>" # required


Migrate database schema:

    python3 migrate.py db init
    python3 migrate.py db migrate
    python3 migrate.py db upgrade

Run:

    python3 run.py
