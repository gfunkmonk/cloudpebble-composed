FROM gfunkmonk/alpine-python-node:3.10 AS squashme
SHELL ["/bin/bash", "-c"]

RUN apk update && apk add --no-cache pixman-dev glib-dev dtc-dev gnutls-dev && apk add --no-cache --virtual .build-deps findutils make libtool \ 
 zlib-dev gcc g++ automake git curl make xz python2-dev && rm -rf /var/cache/apk/* 

#RUN git clone https://github.com/gfunkmonk/qemu && cd /qemu && \
RUN mkdir /qemu && cd /qemu && \
  curl -L https://github.com/gfunkmonk/qemu/archive/v2.5.0-pebble5b.tar.gz | tar xz --strip 1 && \
  ./configure \
     #--extra-ldflags=-g \
     --enable-debug --disable-werror --target-list="arm-softmmu" \
     #--disable-libiscsi --disable-libnfs --disable-libusb --disable-usb-redir \
     #--disable-strip --disable-xen --disable-kvm --disable-user --disable-docs \
     #--disable-gtk --disable-linux-aio --disable-curl --disable-curses --disable-vhdx \
     --extra-cflags=-std=gnu99 \
     --extra-cflags=-DSTM32_UART_NO_BAUD_DELAY \
     #--extra-cflags=-DSTM32_UART_ENABLE_OVERRUN \
     --enable-vnc \
     --disable-sdl \ 
     #--enable-tcg-interpreter --with-coroutine=gthread --enable-debug-tcg \
     #--disable-uuid --enable-fdt --disable-libusb  --disable-usb-redir \
     #--disable-vte  --disable-vhdx --disable-libssh2 --enable-gnutls \
     #--enable-nettle --disable-docs --disable-kvm --disable-strip \
     #--disable-xen --disable-kvm --disable-gtk --disable-curses \
  && make clean \
  && make -j4

RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch master --recursive
#RUN git clone https://github.com/pebble/pypkjs.git --depth 1 --branch v1.1.1 --recursive

RUN pip install virtualenv && \
  virtualenv /pypkjs/.env && \
  . /pypkjs/.env/bin/activate \
  && pip install -r /pypkjs/requirements.txt

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /qemu-tintin-images && cd /qemu-tintin-images && \
  curl -L https://github.com/pebble/qemu-tintin-images/archive/v4.3.tar.gz | \
  tar xz --strip 1

RUN apk del .build-deps

COPY . /code

#FROM scratch
#COPY --from=squashme / /
WORKDIR /code

ENV QEMU_DIR=/qemu QEMU_BIN=/qemu/arm-softmmu/qemu-system-arm \ 
  PKJS_BIN=/pypkjs/phonesim.py PKJS_VIRTUALENV=/pypkjs/.env QCON_PORT=80 \ 
  QEMU_IMAGE_ROOT=/qemu-tintin-images

EXPOSE $QCON_PORT
CMD ["python", "controller.py"]
