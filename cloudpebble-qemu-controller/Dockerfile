#FROM python:2.7.16 AS squashme
#FROM gfunkmonk/python2:bionic AS build
FROM gfunkmonk/python2:bionic AS squashme
#FROM gfunkmonk/qemu-base:xenial AS squashme
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
  libglib2.0-dev libpixman-1-dev libfdt-dev gnutls-dev findutils make \
  pkgconf zlib1g-dev device-tree-compiler libbluetooth-dev \ 
  binutils-arm-none-eabi --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/beckus/qemu_stm32.git qemu/ && cd /qemu && \
RUN git clone https://github.com/gfunkmonk/qemu && cd /qemu && \
#RUN mkdir /qemu && cd /qemu && \
#  curl -L https://github.com/gfunkmonk/qemu/archive/v2.5.0-pebble5b.tar.gz | tar xz --strip 1 && \
  ./configure \
     --extra-ldflags=-g \
     --enable-debug --disable-werror --target-list="arm-softmmu" \
     --disable-libiscsi --disable-libnfs --disable-libusb --disable-usb-redir \
     --disable-strip --disable-xen --disable-kvm --disable-user --disable-docs \
     --disable-gtk --disable-linux-aio --disable-curl --disable-curses --disable-vhdx \
     #--extra-cflags=-std=gnu99 \
     #--extra-cflags=-DSTM32_UART_NO_BAUD_DELAY \
     #--extra-cflags=-DSTM32_UART_ENABLE_OVERRUN \
     --enable-vnc \
     --disable-sdl \
	&& \
  make clean && \
  make -j4

#FROM gfunkmonk/python2:bionic AS squashme
#COPY --from=build /qemu /qemu

RUN apt-get update && apt-get install -y --no-install-recommends \
  libglib2.0-dev libfdt-dev libpixman-1-dev libbluetooth-dev

#RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch v1.1.1 --recursive
#RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch
#master --recursive
RUN git clone https://github.com/gfunkmonk/pypkjs.git --depth 1 --branch master --recursive \
&& cd pypkjs/ && git revert --hard 42ae814 && cd ..

RUN pip install --no-cache virtualenv
RUN virtualenv /pypkjs/.env && . /pypkjs/.env/bin/activate && pip install -r /pypkjs/requirements.txt

RUN mkdir /qemu-tintin-images && cd /qemu-tintin-images && \
  curl -L https://github.com/gfunkmonk/qemu-tintin-images/archive/v4.3.tar.gz | tar xz --strip 1

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get remove --purge git curl xz-utils -y && apt-get autoremove --purge -y

COPY . /code
FROM scratch
COPY --from=squashme / /
WORKDIR /code

ENV QEMU_DIR=/qemu QEMU_BIN=/qemu/arm-softmmu/qemu-system-arm PKJS_BIN=/pypkjs/phonesim.py \
  PKJS_VIRTUALENV=/pypkjs/.env QCON_PORT=80 QEMU_IMAGE_ROOT=/qemu-tintin-images

EXPOSE $QCON_PORT

CMD ["python", "controller.py"]
