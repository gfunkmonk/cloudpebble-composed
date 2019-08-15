FROM python:2.7.16
MAINTAINER Katharine Berry <katharine@pebble.com>

RUN apt-get update && apt-get install -y build-essential cmake python2-dev npm ninja-build

# ycmd
RUN git clone https://github.com/Valloric/ycmd.git /ycmd && cd /ycmd && \
  git reset --hard c5ae6c2915e9fb9f7c18b5ec9bf8627d7d5456fd && \
  git submodule update --init --recursive && \
  ./build.sh --clang-completer

#RUN git clone https://github.com/Valloric/ycmd.git /ycmd && cd /ycmd && \
#  git submodule update --init --recursive && \
#  python2 build.py --clangd-completer --ts-completer --ninja --js-completer

#RUN git clone https://github.com/Valloric/ycmd.git -b clang-format /ycmd && cd /ycmd && \
#  git submodule update --init --recursive && \
#  ./build.py --clang-completer

# Grab the toolchain
RUN curl -o /tmp/arm-cs-tools.tar https://cloudpebble-vagrant.s3.amazonaws.com/arm-cs-tools-stripped.tar && \
  tar -xf /tmp/arm-cs-tools.tar -C / && rm /tmp/arm-cs-tools.tar

# Node stuff.

ENV NODE_VERSION=9.11.2 NPM_CONFIG_LOGLEVEL=info
RUN mkdir ~/.gnupg && echo "disable-ipv6" >> ~/.gnupg/dirmngr.conf

# gpg keys listed at https://github.com/nodejs/node
RUN set -ex \
  && for key in \
    9554F04D7259F04124DE6B476D5A82AC7E37093B \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    0034A06D9D9B0064CE8ADF6BF1747F4AD2306D93 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
  ; do \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
  done

RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --verify SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
  && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc

RUN npm install npm -g

ENV SDK_TWO_VERSION=2.9

# Install SDK 2
RUN mkdir /sdk2 && \
  curl -L "https://web.archive.org/web/20171221154852/http://assets.getpebble.com.s3-website-us-east-1.amazonaws.com/sdk2/PebbleSDK-${SDK_TWO_VERSION}.tar.gz" | \
  tar --strip-components=1 -xz -C /sdk2

ENV SDK_THREE_VERSION=4.3

# Install SDK 3
RUN mkdir /sdk3 && \
  curl -L "https://pebble.rip/SDKCores/sdk-core-${SDK_THREE_VERSION}.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk3

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

ENV PATH="$PATH:/arm-cs-tools/bin" YCMD_PEBBLE_SDK2=/sdk2/ YCMD_PEBBLE_SDK3=/sdk3/ \
  YCMD_STDLIB=/arm-cs-tools/arm-none-eabi/include/ \
  DEBUG=yes YCMD_PORT=80 YCMD_BINARY=/ycmd/ycmd/__main__.py \
  YCMD_DEFAULT_SETTINGS=/ycmd/ycmd/default_settings.json

CMD ["python", "proxy.py"]
