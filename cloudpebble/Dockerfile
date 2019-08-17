FROM python:2.7.16
MAINTAINER Katharine Berry <katharine@pebble.com>

ENV NPM_CONFIG_LOGLEVEL=info NODE_VERSION=10.15.3 DJANGO_VERSION=1.6 NODEJS_CHECK_SIGNATURES=no

# C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
# Node stuff.

# gpg keys listed at https://github.com/nodejs/node


RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
#  && gpg --verify SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
  && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc

RUN npm install -g npm jshint

# Django stuff

# Fix broken sources.list (stretch repositories)
#RUN printf "deb http://ftp.debian.org/debian/ stretch main contrib non-free\ndeb-src http://ftp.debian.org/debian/ stretch main contrib non-free\ndeb http://security.debian.org stretch/updates main\ndeb-src http://security.debian.org stretch/updates main" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    gettext \
    postgresql-client libpq-dev \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2 django=="$DJANGO_VERSION"

EXPOSE 8000

# CloudPebble stuff
RUN npm install -g bower && echo '{"allow_root": true}' > /root/.bowerrc

# Grab the toolchain
RUN curl -o /tmp/arm-cs-tools.tar https://cloudpebble-vagrant.s3.amazonaws.com/arm-cs-tools-stripped.tar && \
  tar -xf /tmp/arm-cs-tools.tar -C / && rm /tmp/arm-cs-tools.tar

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV SDK_TWO_VERSION=2.9

# Install SDK 2
RUN mkdir /sdk2 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-${SDK_TWO_VERSION}.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk2

ENV SDK_THREE_CHANNEL=release
ENV SDK_THREE_VERSION=4.3

# Install SDK 3
RUN mkdir /sdk3 && \
  curl -L "https://binaries.rebble.io/sdk-core/${SDK_THREE_CHANNEL}/sdk-core-${SDK_THREE_VERSION}.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk3

# Install SDK 3 Node dependencies
RUN cd /sdk3 && npm install
ENV WAF_NODE_PATH=/sdk3/node_modules

COPY . /code
WORKDIR /code

# Bower is awful.
RUN rm -rf bower_components && cd /tmp && python /code/manage.py bower install && mv bower_components /code/

RUN python manage.py compilemessages 

RUN make -C /code/c-preload

CMD ["sh", "docker_start.sh"]
