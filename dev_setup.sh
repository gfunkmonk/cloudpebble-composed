#!/bin/bash
chmod 700 /root/.gnupg/
chmod 600 /root/.gnupg/*
# Run the general build.
docker-compose build
# Do this in the mounted directory, since the Dockerfile did it in a folder we
# mask by mounting over it.
docker-compose run web sh -c "rm -rf bower_components && cd /tmp && python /code/manage.py bower install && mv bower_components /code/"
# Stop everything again.
docker-compose stop
