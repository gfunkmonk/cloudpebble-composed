FROM gfunkmonk/alpine-python-node:3.10 AS squashme
SHELL ["/bin/bash", "-c"]

RUN apk update && apk add --no-cache memcached postgresql-client postgresql-dev gettext curl git wget xz \
 gcc g++ make && apk add --no-cache --virtual .build-deps zlib-dev jpeg-dev linux-headers musl-dev python2-dev && \
 rm -rf /var/cache/apk/*

RUN npm install -g jshint bower && echo '{"allow_root": true}' > /root/.bowerrc

EXPOSE 8000

ADD requirements.txt /tmp/requirements.txt
RUN pip install psycopg2 django==1.9.12 && pip install --no-cache-dir -r /tmp/requirements.txt

# Grab the toolchain
RUN mkdir /arm-cs-tools && \
  curl -L "https://gfunkmonk.s3.amazonaws.com/arm-cs-tools-4.9-2017.01.tar.xz" | \
  tar --strip-components=1 -xJ -C /arm-cs-tools

# Install SDK 2
RUN mkdir /sdk2 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-2.9.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk2

# Install SDK 3
RUN mkdir /sdk3 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-4.3.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk3

# Install SDK 3 Node dependencies
RUN cd /sdk3 && npm install
ENV WAF_NODE_PATH=/sdk3/node_modules

COPY . /code
WORKDIR /code

# Bower is awful.
RUN rm -rf bower_components && cd /tmp && python /code/manage.py bower install && mv bower_components /code/ && mv /code/bower_components/codemirror /code/bower_components/CodeMirror/
RUN python manage.py compilemessages
RUN make -C /code/c-preload

RUN apk del .build-deps

#FROM scratch
#COPY --from=squashme / /
#ENV WAF_NODE_PATH=/sdk3/node_modules
#WORKDIR /code

CMD ["sh", "docker_start.sh"]
