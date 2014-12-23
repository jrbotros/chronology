import json
import requests
import unittest

from metis import app  # noqa
from pykronos import KronosClient

import logging; logging.basicConfig()
log = logging.getLogger(__name__)


class MetisServerTestCase(unittest.TestCase):
  '''
  Unit tests for all available `Operator` types.
  '''
  def setUp(self):
    self.kronos_client = KronosClient('http://localhost:9191')
    self.index_path = '1.0/index'
    self.source_path = '1.0/sources'
    self.streams_path = '1.0/streams/kronos'
    self.schema_path = '1.0/streams/kronos/%s'
    self.query_path = '1.0/query'
    self.server_url = 'http://localhost:9192/%s'
    self.executor = None

  def index(self):
    response = requests.get(self.server_url % self.index_path)
    self.assertEqual(response.status_code, requests.codes.ok)
    return response.json()

  def data_sources(self):
    response = requests.get(self.server_url % self.source_path)
    self.assertEqual(response.status_code, requests.codes.ok)
    return response.json()

  def get_streams(self):
    response = requests.get(self.server_url % self.streams_path)
    self.assertEqual(response.status_code, requests.codes.ok)
    return response.json()

  def schema(self):
    url = self.server_url % self.schema_path % 'test_schema.test1'
    response = requests.get(url)
    self.assertEqual(response.status_code, requests.codes.ok)
    return response.json()

  def query(self, plan):
    response = requests.post(self.server_url % self.query_path,
                             data=json.dumps({'plan': plan,
                                              'executor': self.executor}))
    if response.status_code != requests.codes.ok:
      log.error('Invalid response code for response: %s', response.text)
    self.assertEqual(response.status_code, requests.codes.ok)
    events = []
    for line in response.text.split('\n'):
      line = line.strip()
      if not line:
        continue
      events.append(json.loads(line))
    return events
