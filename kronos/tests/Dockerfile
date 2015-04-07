# Dockerfile for running kronos tests with various backends.

# https://docs.docker.com/articles/dockerfile_best-practices/
# Check for updates:
#   https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
FROM phusion/baseimage:0.9.16

# Install dependencies.
RUN \
  apt-get update && \
  apt-get install -y \
  build-essential \
  libevent-dev \
  libpcre3-dev \
  python-all-dev \
  python-pip \
  python2.7 \
  uuid-dev \
  wget

# Set up Cassandra, Elasticsearch.
RUN echo "deb http://debian.datastax.com/community stable main" | \
  sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
RUN echo "deb http://packages.elasticsearch.org/elasticsearch/1.5/debian \
  stable main" | \
  sudo tee -a /etc/apt/sources.list
RUN wget -qO - https://packages.elasticsearch.org/GPG-KEY-elasticsearch | \
  sudo apt-key add -

RUN apt-get update && \
  apt-get install -y \
  openjdk-7-jre \
  dsc20=2.0.11-1 \
  cassandra=2.0.11 \
  elasticsearch

COPY chronology/kronos/requirements.txt /requirements.txt
RUN sudo pip install -r /requirements.txt

COPY chronology /chronology
WORKDIR /chronology/kronos

RUN mkdir /etc/service/cassandra
COPY run-cassandra.sh /etc/service/cassandra/run
RUN mkdir /etc/service/elasticsearch
COPY run-elasticsearch.sh /etc/service/elasticsearch/run
COPY setup-elasticsearch.sh /etc/my_init.d/elasticsearch.sh

CMD ["/sbin/my_init", "--quiet", "--", "sh", "-c", "sleep 10; ./runtests.py all"]