#!/bin/bash
source .env
cp .env cloudpebble/
# Run the general build.
docker-compose build --compress --pull --force-rm --no-cache
#docker-compose build --pull
# Do this in the mounted directory, since the Dockerfile did it in a folder we
# mask by mounting over it.
docker-compose run web sh -c "rm -rf bower_components && cd /tmp && python /code/manage.py bower install && cp -R bower_components/ /code/ && rm -fr /tmp/bower_components/"
# Stop everything again.
docker-compose stop
