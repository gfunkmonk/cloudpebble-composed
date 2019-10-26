#!/bin/bash
source .env
cp .env cloudpebble/.env
# Run the general build.
#docker build --compress --force-rm --pull --squash -f cloudpebble-qemu-controller/Dockerfile -t cloudpebble_qemu:latest cloudpebble-qemu-controller/
#docker build --compress --force-rm --pull --squash -f cloudpebble-ycmd-proxy/Dockerfile -t cloudpebble_ycmd:latest cloudpebble-ycmd-proxy/
docker-compose build --squash --compress --force-rm --pull --parallel
#docker-compose build --pull
# Do this in the mounted directory, since the Dockerfile did it in a folder we
# mask by mounting over it
docker-compose run web sh -c "rm -rf bower_components && cd /tmp && python /code/manage.py bower install && cp -R bower_components/ /code/ && rm -f /tmp/bower_components/"
#docker-compose run web sh -c "python manage.py collectstatic --noinput -c"
# Stop everything again.
docker-compose stop
