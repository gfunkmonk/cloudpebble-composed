FROM alpine:latest

COPY memcached.sh /memcached.sh
RUN apk --no-cache add memcached && chmod +x /memcached.sh

USER memcached
EXPOSE 11211
CMD ["/memcached.sh"]
