FROM gfunkmonk/alpine-python-node:3.10 AS squashme
SHELL ["/bin/bash", "-c"]
VOLUME ["/opt/node_modules"]

RUN apk update && apk add --no-cache memcached postgresql-client postgresql-dev gettext git freetype \
 gcc g++ && apk add --no-cache --virtual .build-deps zlib-dev jpeg-dev linux-headers musl-dev python2-dev xz wget make curl && \
 rm -rf /var/cache/apk/* 
##&& curl -L https://unpkg.com/@pnpm/self-installer | node 

#ADD bowerrc /tmp/bowerrc
RUN npm install -g jshint bower && printf '{"allow_root": true}' > /root/.bowerrc 

#ADD package.json /tmp/package.json
#RUN cd /tmp && npm install
#RUN mkdir -p /opt/npm && cp -a /tmp/node_modules /opt/npm/ && rm -fr /code/node_modules/
#ENV NODE_MODULES_PATH /opt/npm/node_modules

EXPOSE 8000

ADD requirements.txt /tmp/requirements.txt
RUN pip install psycopg2 django==1.9.12 && pip install --no-cache-dir -r /tmp/requirements.txt

# Grab the toolchain
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
  wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.29-r0/glibc-2.29-r0.apk && \
  apk add glibc-2.29-r0.apk && rm glibc-2.29-r0.apk && \
  curl -L "http://pebble.gfunkmonk.info/secret/arm-cs-tools/GNU/arm-cs-tools-stripped.tar.xz" | tar -xJ -C /

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
RUN python /code/manage.py bower cache clean
RUN rm -rf bower_components && cd /tmp && python /code/manage.py bower install && mv bower_components /code/ && cd /code/bower_components/
RUN python manage.py compilemessages
RUN make -C /code/c-preload

RUN apk del .build-deps && rm -rf /var/cache/apk/*

FROM scratch
COPY --from=squashme / /
ENV WAF_NODE_PATH=/sdk3/node_modules
#ENV NODE_MODULES_PATH /opt/npm/node_modules
WORKDIR /code

#RUN python manage.py collectstatic --noinput -c

CMD ["sh", "docker_start.sh"]
