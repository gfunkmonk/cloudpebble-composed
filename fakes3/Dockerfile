FROM debian:buster-slim AS squashme

ENV DEBIAN_FRONTEND noninteractive

# install Ruby
RUN apt-get update && apt-get install -yqq ruby rubygems-integration --no-install-recommends

# install fake-s3
RUN gem install fakes3 -v 0.2.5

# run fake-s3
RUN mkdir -p /fakes3_root
FROM debian:buster-slim
COPY --from=squashme / /
ENTRYPOINT ["/usr/local/bin/fakes3"]
CMD ["-r",  "/fakes3_root", "-p",  "4569"]
EXPOSE 4569
