FROM python:2.7.16-buster
MAINTAINER Katharine Berry <katharine@pebble.com>
SHELL ["/bin/bash", "-c"]

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get update && apt-get install -y \
    gettext memcached nodejs \
    postgresql-client libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN npm install -g npm jshint
RUN pip install psycopg2 django==1.6.2

EXPOSE 8000

# CloudPebble stuff
RUN npm install -g bower && echo '{"allow_root": true}' > /root/.bowerrc

# Grab the toolchain
RUN curl -o /tmp/arm-cs-tools.tar https://cloudpebble-vagrant.s3.amazonaws.com/arm-cs-tools-stripped.tar && \
  tar -xf /tmp/arm-cs-tools.tar -C / && rm /tmp/arm-cs-tools.tar

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

RUN service memcached start
CMD ["sh", "docker_start.sh"]
