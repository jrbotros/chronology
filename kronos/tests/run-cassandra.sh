#!/bin/sh

exec /sbin/setuser cassandra /usr/sbin/cassandra -f >> /var/log/cassandra/system.log 2>&1
