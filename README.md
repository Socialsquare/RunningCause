# RunningCause
A django project to provide runners an easy to use interface to gather money 
from sponsors when running for a good cause.


# Requirements:

 * redis
 * celery
 * postgresql


# celery

	celery -A RunningCause worker --loglevel=debug


# deployment to heroku

	git push heroku master:master
	heroku ps:scale web=1 --app masanga-runners