#FROM python:2.7.16 AS squashme
#FROM gfunkmonk/dev:xenial AS squashme
FROM gfunkmonk/python2:bionic AS squashme
#FROM gfunkmonk/python:trusty-mini2 AS build
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
   cmake libtinfo5 git curl xz-utils wget \
   --no-install-recommends && rm -rf /var/lib/apt/lists/

# ycmd
RUN git clone https://github.com/Valloric/ycmd.git /ycmd && cd /ycmd && \
  git reset --hard c5ae6c2915e9fb9f7c18b5ec9bf8627d7d5456fd && \
  git submodule update --init --recursive && \
  ./build.sh --clang-completer

#FROM gfunkmonk/python:trusty-mini2 AS squashme
#COPY --from=build /ycmd /ycmd
#COPY --from=build /usr/lib/llvm-3.4/lib/libclang.so /ycmd

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  apt-get update && apt-get install --no-install-recommends -y \
  nodejs && rm -rf /var/lib/apt/lists/

# Grab the toolchain
RUN curl -o /tmp/arm-cs-tools-4.9-2017.01.tar.xz https://gfunkmonk.s3.amazonaws.com/arm-cs-tools-4.9-2017.01.tar.xz && \
  tar -xJf /tmp/arm-cs-tools-4.9-2017.01.tar.xz -C / && rm /tmp/arm-cs-tools-4.9-2017.01.tar.xz

# Install SDK 2
RUN mkdir /sdk2 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-2.9.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk2

# Install SDK 3
RUN mkdir /sdk3 && \
  curl -L "https://binaries.rebble.io/sdk-core/release/sdk-core-4.3.tar.bz2" | \
  tar --strip-components=1 -xj -C /sdk3

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

#RUN apt remove --purge curl xz-utils git -y && apt-get autoremove --purge -y

COPY . /code
FROM scratch
COPY --from=squashme / /
WORKDIR /code

ENV PATH="$PATH:/arm-cs-tools/bin" YCMD_PEBBLE_SDK2=/sdk2/ YCMD_PEBBLE_SDK3=/sdk3/ \
  YCMD_STDLIB=/arm-cs-tools/arm-none-eabi/include/ \
  DEBUG=yes YCMD_PORT=80 YCMD_BINARY=/ycmd/ycmd/__main__.py \
  YCMD_DEFAULT_SETTINGS=/ycmd/ycmd/default_settings.json

CMD ["python", "proxy.py"]
