FROM alpine:3.5

ARG HOST_NAME=s3.amazonaws.com
ENV FAKES3_VERSION 2.0.0

RUN mkdir -p /fakes3_root
WORKDIR /fakes3_root
VOLUME ["/fakes3_root"]

EXPOSE 4569

RUN apk --no-cache add ruby ruby-io-console && \
  gem install --no-rdoc --no-ri fakes3 -v ${FAKES3_VERSION} && \
  rm -rf /var/cache/apk/*

ENTRYPOINT ["fakes3", "-r", "/fakes3_root", "-p", "4569", "--license", "$FAKES3_KEY"]
