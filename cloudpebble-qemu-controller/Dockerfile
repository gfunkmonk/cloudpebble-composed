FROM python:2.7.16
MAINTAINER Katharine Berry <katharine@pebble.com>

RUN apt-get update && apt-get install -y \
  libglib2.0-dev libpixman-1-dev libfdt-dev gnutls-dev libsdl2-dev

ENV QEMU_VERSION 2.5.0-pebble5
  
RUN mkdir /qemu && cd /qemu && \
  curl -L https://github.com/gfunkmonk/qemu/archive/v${QEMU_VERSION}.tar.gz | tar xz --strip 1 && \
  ./configure --disable-werror --enable-debug --target-list="arm-softmmu" \
#  --extra-cflags="-DSTM32_UART_NO_BAUD_DELAY -std=gnu99" --enable-vnc --disable-sdl 
  #    --enable-tcg-interpreter \
       --extra-ldflags=-g \
#      --with-coroutine=gthread \
#      --enable-debug-tcg \
       --enable-debug --disable-werror --target-list="arm-softmmu" \
#      --extra-cflags=-DDEBUG_CLKTREE --extra-cflags=-DDEBUG_STM32_RCC \
#      --extra-cflags=-DDEBUG_STM32_UART \
#      --extra-cflags=-DDEBUG_GIC 
       --enable-vnc \
       --with-sdlabi=2.0 \
       --enable-sdl \
          && \
  make clean && \
  make -j4

ENV PYPKJS_VERSION 1.1.1

#RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch v$PYPKJS_VERSION --recursive
RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch master --recursive

RUN virtualenv /pypkjs/.env && . /pypkjs/.env/bin/activate && pip install -r /pypkjs/requirements.txt

ENV FIRMWARE_VERSION 4.3

RUN mkdir /qemu-tintin-images && cd /qemu-tintin-images && \
  curl -L https://github.com/pebble/qemu-tintin-images/archive/v${FIRMWARE_VERSION}.tar.gz | tar xz --strip 1


ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

ENV QEMU_DIR=/qemu QEMU_BIN=/qemu/arm-softmmu/qemu-system-arm PKJS_BIN=/pypkjs/phonesim.py \
  PKJS_VIRTUALENV=/pypkjs/.env QCON_PORT=80 QEMU_IMAGE_ROOT=/qemu-tintin-images

EXPOSE $QCON_PORT

CMD ["python", "controller.py"]
