#!/bin/sh
sleep 1
if [ ! -z "$RUN_WEB" ]; then
	# Make sure the database is up to date.
	echo "Performing database migration."
	#python manage.py syncdb --noinput
        #python manage.py makemigrations
	python manage.py migrate --fake-initial

	python manage.py runserver 0.0.0.0:$PORT --nostatic
elif [ ! -z "$RUN_CELERY" ]; then
	sleep 2
	#C_FORCE_ROOT=true celery -A cloudpebble worker --loglevel=info
	C_FORCE_ROOT=true python celery_start.py
else
	echo "Doing nothing!"
	exit 1
fi
