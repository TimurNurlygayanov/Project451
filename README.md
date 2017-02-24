# Project451
To start application:

#### Usage
Install dependencies:

    pip3 install -r requirements.txt


Set environment variables:

    export HOST="<Host address>" # otherwise it will use localhost
    export PORT="<Port on which app will be deployed>" # otherwise it will use 5000
    export SENDGRID_API_KEY="<Your Sendgrid API key>" # required
    export DATABASE_URI="<sql>://<username>:<password>@<host>:<port>/<database>" # required


Migrate database schema:

    python3 migrate.py db init
    python3 migrate.py db migrate
    python3 migrate.py db upgrade

Run:

    python3 run.py