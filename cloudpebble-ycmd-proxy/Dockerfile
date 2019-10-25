FROM gfunkmonk/python2:disco AS squashme
SHELL ["/bin/bash", "-c"]

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get update && apt-get install -y \
    cmake libtinfo5 git curl xz-utils wget libclang-dev nodejs \
    --no-install-recommends && rm -rf /var/lib/apt/lists/

# ycmd
RUN git clone https://github.com/Valloric/ycmd.git /ycmd && cd /ycmd && \
#RUN git clone https://github.com/gfunkmonk/ycmd.git -b cloudpebble /ycmd && cd /ycmd && \
  #git reset --hard c5ae6c2915e9fb9f7c18b5ec9bf8627d7d5456fd && \
  git reset --hard 10c456c6e32487c2b75b9ee754a1f6cc6bf38a4f && \
  git submodule update --init --recursive && \
  #./build.sh --clang-completer
  #python build.py --clang-completer --system-libclang
  python build.py --clang-completer --system-libclang	
  #python build.py --clang-completer

# Grab the toolchain
RUN mkdir /arm-cs-tools \
  && curl -L "https://gfunkmonk.s3.amazonaws.com/arm-cs-tools-7.4-2019.02.tar.xz" | \
  tar --strip-components=1 -xJ -C /arm-cs-tools

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

RUN apt remove --purge curl xz-utils git libmagickcore-dev libmagickwand-dev \
  autotools-dev bzr mercurial subversion python3 python3-minimal hicolor-icon-theme \ 
  -y && apt-get autoremove --purge -y

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
