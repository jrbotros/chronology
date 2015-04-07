#!/bin/sh

CONFIG_DIR=/usr/share/elasticsearch/config
mkdir -p $CONFIG_DIR
ln -s /etc/elasticsearch/elasticsearch.yml $CONFIG_DIR/elasticsearch.yml
ln -s /etc/elasticsearch/logging.yml $CONFIG_DIR/logging.yml
