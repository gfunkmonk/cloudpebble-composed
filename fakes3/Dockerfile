FROM debian:buster-slim AS squashme

MAINTAINER Larry Howard <larry.howard@vanderbilt.edu>

ENV DEBIAN_FRONTEND noninteractive

# install Ruby
RUN apt-get update && apt-get install -yqq ruby rubygems-integration --no-install-recommends

# install fake-s3
RUN gem install fakes3 -v 0.2.5 --no-doc
#RUN gem install fakes3 --no-doc

# run fake-s3
RUN mkdir -p /fakes3_root
FROM scratch
COPY --from=squashme / /
ENTRYPOINT ["/usr/local/bin/fakes3"]
CMD ["-r",  "/fakes3_root", "-p",  "4569"]
#CMD ["-r",  "/fakes3_root", "-p",  "4569", "--license", "$FAKES3_KEY"]
EXPOSE 4569
