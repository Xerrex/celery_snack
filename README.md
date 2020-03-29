# Flask + Celery snack

Code for testing working with celery, for future developments.

## Acknowledgement

* Checkout thcheckout this article: [Using Celery With Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask)

## Technologies/Tools used & needed.

* **[Python](https://www.python.org/downloads/)** - A programming language.
* **[Flask](flask.pocoo.org/)** - A microframework for Python.
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments

### NB

* Docker is a work around to not having to install Redis
* **[Docker](https://www.docker.com/)** - set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.

## Quick setup: linux based OS

* **Clone or this download repo then 'cd' into the dir**

* **Create virtual environment**

    ```bash

    virtualenv -p python3 venv
    ```

* **Create a '.env' file & add the following**

    ```bash
    touch .env
    ```

    Add the following lines to the file

    ```text
    source venv/bin/activate
    export FLASK_APP=app.py
    export FLASK_DEBUG=1
    export FLASK_ENV=development
    export CELERY_BROKER_URL='redis://0.0.0.0:6379/0'
    export CELERY_RESULT_BACKEND='redis://0.0.0.0:6379/0'
    ```

* **Create an instance dir & config.py file, add the following**

    ```bash
    mkdir instance && touch config.py
    ```

    **add the following**

    ```python
    SECRET_KEY=<your value>
    MAIL_USERNAME=<your gmail username>
    MAIL_PASSWORD=<your gmail password>
    ```

* **Activate virtual environment & export variables**

    ```bash
    source .env
    ```

* **Install Dependancies**.

    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

## Running the app

* **Open the 3 terminal windows in the current dir**

* **Start redis on one terminal**

    ```bash
    chmod +x run-redis.sh && ./run-redis.sh
    ```

* **Run celery worker on another terminal**

    ```bash
    celery worker -A app.celery --loglevel=info
    ```

* **Run flask app on the last window**

    ```bash
    flask run
    ```

## Go to the browser and open 127.0.0.1:5000

* fun fact: minimise all windows to view changes in the windows.
