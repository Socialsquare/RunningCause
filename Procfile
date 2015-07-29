web: gunicorn RunningCause.wsgi:application --log-file -
worker: celery worker --app=RunningCause.celery -l info
