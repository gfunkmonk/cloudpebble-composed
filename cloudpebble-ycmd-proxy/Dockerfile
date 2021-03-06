FROM gfunkmonk/alpine-python-node:3.10 AS squashme
SHELL ["/bin/bash", "-c"]

RUN apk update && apk add --no-cache ncurses-dev && apk add --no-cache --virtual .build-deps gcc g++ make automake git curl xz wget cmake python2-dev \ 
  && rm -rf /var/cache/apk/* 
  #&& curl -L https://unpkg.com/@pnpm/self-installer | node

# ycmd
ADD CMakeLists-v9.txt /tmp/CMakeLists.txt

RUN git clone https://github.com/Valloric/ycmd.git /ycmd && cd /ycmd && \
#RUN git clone https://github.com/gfunkmonk/ycmd.git -b cloudpebble /ycmd && cd /ycmd && \
  #git reset --hard c5ae6c2915e9fb9f7c18b5ec9bf8627d7d5456fd && \
  git reset --hard 10c456c6e32487c2b75b9ee754a1f6cc6bf38a4f && \
  git submodule update --init --recursive && \
  cp /tmp/CMakeLists.txt cpp/ycm/CMakeLists.txt && \
  #./build.sh --clang-completer
  #python build.py --clang-completer --system-libclang
  #python build.py --clang-completer --system-libclang	
  python build.py --clang-completer 

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

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apk del .build-deps && rm -rf /var/cache/apk/*

RUN ln -sf /ycmd/libclang.so /ycmd/libclang.so.9 && \
  ln -sf /ycmd/libclang.so /ycmd/libclang.so.7 && \
  ln -sf /ycmd/libclang.so /ycmd/libclang.so.5

COPY . /code
FROM scratch
COPY --from=squashme / /
WORKDIR /code

ENV PATH="$PATH:/arm-cs-tools/bin" \
  YCMD_PEBBLE_SDK2=/sdk2/ YCMD_PEBBLE_SDK3=/sdk3/ \
  YCMD_STDLIB=/arm-cs-tools/arm-none-eabi/include/ \
  DEBUG=yes YCMD_PORT=80 YCMD_BINARY=/ycmd/ycmd/__main__.py \
  YCMD_DEFAULT_SETTINGS=/ycmd/ycmd/default_settings.json

ENV PATH="$PATH:/ycmd"

CMD ["python", "proxy.py"]
