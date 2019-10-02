FROM python:2.7 AS squashme
#FROM gfunkmonk/python2:disco AS squashme
SHELL ["/bin/bash", "-c"]

ENV NPM_CONFIG_LOGLEVEL=info NODE_VERSION=10.15.3 DJANGO_VERSION=1.6 NODEJS_CHECK_SIGNATURES=no

#RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
#  apt-get install -y nodejs

RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
#  && gpg --verify SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
  && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc

RUN npm install -g npm jshint

# Django stuff
RUN apt-get update && apt-get install -y \
    gettext memcached postgresql-client libpq-dev curl git wget xz-utils --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2 django=="$DJANGO_VERSION"

EXPOSE 8000

# CloudPebble stuff
RUN npm install -g bower && echo '{"allow_root": true}' > /root/.bowerrc

# Grab the toolchain
RUN curl -o /tmp/arm-cs-tools.tar https://cloudpebble-vagrant.s3.amazonaws.com/arm-cs-tools-stripped.tar && \
  tar -xf /tmp/arm-cs-tools.tar -C / && rm /tmp/arm-cs-tools.tar

#RUN mkdir /arm-cs-tools && curl -L "https://gfunkmonk.s3.amazonaws.com/arm-cs#-tools-4.9-2017.01.tar.xz" | tar --strip-components=1 -xJ -C /arm-cs-tools

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

#RUN apt-get remove --purge wget xz-utils curl autoconf automake libcurl4-openssl-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev -y && apt-get autoremove --purge -y

FROM scratch
COPY --from=squashme / /
ENV WAF_NODE_PATH=/sdk3/node_modules
WORKDIR /code

CMD ["sh", "docker_start.sh"]
