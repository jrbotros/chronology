#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from jia import config

app = config(settings_file='/etc/jia/settings.py')
