# Project451
To start application:

#### Usage
Install dependencies:

* You will need some system packages, so install corresponding packages in your system, like for Ubuntu:

		sudo apt-get install python3 python3-pip postgresql-server-dev-all

* Then install required python3 packages:

		pip3 install -r requirements.txt

* For testing you need additional requirements. For install it just run:

    pip3 install -r test-requirements.txt


Set environment variables for application:

    export HOST="<Host address>" # otherwise it will use localhost
    export PORT="<Port on which app will be deployed>" # otherwise it will use 5000
    export DATABASE_URI="<sql>://<username>:<password>@<host>:<port>/<database>" # required

Set environment variables for ui client if needed:

    export HOST_UI="<Host UI address>" # otherwise it will use localhost
    export PORT_UI="<Port on which ui client will be deployed>" # otherwise it will use 5001
    export API_URL="<Url for application api>" # set it if you use custome HOST and PORT variables for app

Migrate database schema:

    python3 migrate.py db upgrade
    python3 migrate.py db migrate

Run:

    python3 run.py

Run UI:

    python3 run_ui.py

Run unit test:

    py.test
