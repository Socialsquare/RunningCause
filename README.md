# RunningCause
A django project to provide runners an easy to use interface to gather money
from sponsors when running for a good cause.

# Development environment

Setting up a development environment on a Ubuntu machine, you'll have to do the
following.

## Python 2.7 and virtualenv

Make sure you have both python 2.7 and the virtualenv tool installed.  

## Install the postgresql dependency

	sudo apt-get install libpq-dev

## Install the Python dependencies

	pip install -r requirements.txt

# Developing on 

`cd` into the project root dir  
`virtualenv -p python2.7 venv` *initialise python 3 virtual environment*  
`. venv/bin/activate` *start the virtual environment*  
`pip install -r requirements.txt` *install required python modules*  
`./manage.py migrate` *initialise the database*  
`./manage.py createsuperuser` *create admin user*  
`./manage.py runserver` *start the app*  

# Production requirements (on heroku)

 * redis
 * celery
 * postgresql

## celery

	celery -A RunningCause worker --loglevel=debug

## Deployment
A webhook is placed on GitHub that asks Heroku to deploy the site whenever
changes are pushed to the ´development´ branch.
