# https://docs.docker.com/articles/dockerfile_best-practices/
FROM ubuntu:14.04

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
  supervisor \
  uuid-dev \
  wget

COPY chronology/kronos/requirements.txt /requirements.txt
RUN sudo pip install -r /requirements.txt

COPY chronology /chronology
WORKDIR /chronology/kronos

RUN python setup.py install
RUN mkdir -p /home/kronos && chown -R kronos:kronos /home/kronos

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
