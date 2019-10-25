FROM gfunkmonk/python2:disco AS squashme
SHELL ["/bin/bash", "-c"]

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  apt-get update && apt-get install -y --no-install-recommends \
  gettext memcached postgresql-client libpq-dev curl git wget xz-utils nodejs libfreetype6 \
  && rm -rf /var/lib/apt/lists/*

RUN npm install -g jshint bower && echo '{"allow_root": true}' > /root/.bowerrc

EXPOSE 8000

ADD requirements.txt /tmp/requirements.txt
RUN pip install psycopg2 django==1.6.2 && \
  pip install --no-cache-dir -r /tmp/requirements.txt

# Grab the toolchain
RUN mkdir /arm-cs-tools && \
  curl -L "https://gfunkmonk.s3.amazonaws.com/arm-cs-tools-7.4-2019.02.tar.xz" | \
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

RUN apt-get remove --purge wget xz-utils autoconf automake libcurl4-openssl-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev autotools-dev \ 
  bzr mercurial subversion python3 python3-minimal hicolor-icon-theme -y && apt-get autoremove --purge -y

FROM scratch
COPY --from=squashme / /

ENV WAF_NODE_PATH=/sdk3/node_modules
WORKDIR /code

CMD ["sh", "docker_start.sh"]
