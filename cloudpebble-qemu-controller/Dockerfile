FROM python:2.7.16-buster	
MAINTAINER Katharine Berry <katharine@pebble.com>
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
  libglib2.0-dev libpixman-1-dev libfdt-dev gnutls-dev \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*
  
RUN mkdir /qemu && cd /qemu && \
  curl -L https://github.com/gfunkmonk/qemu/archive/v2.5.0-pebble5.tar.gz | tar xz --strip 1 && \
  ./configure --disable-werror --enable-debug --target-list="arm-softmmu" \
       --extra-cflags="-DSTM32_UART_NO_BAUD_DELAY -std=gnu99" \
       --enable-tcg-interpreter \
       --extra-ldflags=-g \
       --enable-vnc \
       --disable-sdl  \
	&& \
  make clean && \
  make -j4

#RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch v1.1.1 --recursive
RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch master --recursive

RUN virtualenv /pypkjs/.env && . /pypkjs/.env/bin/activate && pip install -r /pypkjs/requirements.txt

RUN mkdir /qemu-tintin-images && cd /qemu-tintin-images && \
  curl -L https://github.com/pebble/qemu-tintin-images/archive/v4.3.tar.gz | tar xz --strip 1

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

ENV QEMU_DIR=/qemu QEMU_BIN=/qemu/arm-softmmu/qemu-system-arm PKJS_BIN=/pypkjs/phonesim.py \
  PKJS_VIRTUALENV=/pypkjs/.env QCON_PORT=80 QEMU_IMAGE_ROOT=/qemu-tintin-images

EXPOSE $QCON_PORT

CMD ["python", "controller.py"]
