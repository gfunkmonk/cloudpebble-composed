#FROM python:2.7.16
FROM gfunkmonk/python:alpine-builddep AS squashme
SHELL ["/bin/bash", "-c"]

#RUN npm install -g npm jshint jslint

# Django stuff
RUN apk update && apk add --no-cache gettext memcached postgresql-dev nodejs npm git

RUN pip install psycopg2 django==1.6.2

EXPOSE 8000

# CloudPebble stuff
RUN npm install -g bower jshint jslint && echo '{"allow_root": true}' > /root/.bowerrc

# Grab the toolchain
RUN mkdir /arm-cs-tools && curl -L "https://gfunkmonk.s3.amazonaws.com/arm-cs-tools-4.9-2017.01.tar.xz" | tar --strip-components=1 -xJ -C /arm-cs-tools

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install SDK 2
RUN mkdir /sdk2 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-2.9.tar.bz2" | tar --strip-components=1 -xj -C /sdk2

# Install SDK 3
RUN mkdir /sdk3 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-4.3.tar.bz2" | tar --strip-components=1 -xj -C /sdk3

# Install SDK 3 Node dependencies
RUN cd /sdk3 && npm install
ENV WAF_NODE_PATH=/sdk3/node_modules

COPY . /code
WORKDIR /code

# Bower is awful.
RUN rm -rf bower_components && cd /tmp && python /code/manage.py bower install && mv bower_components /code/
RUN python manage.py compilemessages
RUN make -C /code/c-preload

#RUN apt-get remove --purge git curl xz-utils -y && apt-get autoremove --pu
RUN apk del curl xz
FROM scratch
COPY --from=squashme / /
ENV WAF_NODE_PATH=/sdk3/node_modules
WORKDIR /code
#RUN service memcached start
CMD ["sh", "docker_start.sh"]
