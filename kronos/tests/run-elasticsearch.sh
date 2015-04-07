#!/bin/sh

exec /sbin/setuser elasticsearch /usr/share/elasticsearch/bin/elasticsearch >> /var/log/elasticsearch/system.log 2>&1
