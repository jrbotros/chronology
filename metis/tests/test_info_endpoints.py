from pykronos.client import KronosClient
from tests.server import MetisServerTestCase


class InfoEndpointsTestCase(MetisServerTestCase):

  def test_index(self):
    response = self.index()
    self.assertEquals(response, {'status': 'metisd', 'version': '0.1 alpha'})

  def test_data_sources(self):
    response = self.data_sources()
    self.assertEquals(response, {'status': 'OK', 'sources': {
      'kronos': {'pretty_name': 'Kronos',
                 'type': 'metis.core.query.kronos.source.KronosSource'}}})

  def test_get_streams(self):
    # Make two streams
    self.kronos_client.put({
      'test_get_streams.test1': [
        {'foo':'bar'}
      ],
      'test_get_streams.test2': [
        {'bat': 'lala'}
      ]
    })
    response = self.get_streams()
    self.assertIn('test_get_streams.test1', response['streams'])
    self.assertIn('test_get_streams.test2', response['streams'])

  def test_schema(self):
    # Put some events
    self.kronos_client.put({
      'test_schema.test1': [
        {'foo':'bar'},
        {'bat': True},
        {'lala': {
            'haha': 123
          }
        }
      ]
    })
    response = self.schema()
    self.assertEquals(response, {
      'schema': {
        '$schema': u'http://json-schema.org/draft-04/schema',
        'properties': {
          '@id': {
            'type': 'string'
          },
          '@library': {
            'properties': {
              'name': {
                'type': 'string'
              },
              'version': {
                'type': 'string'
              }
            },
            'required': [
              'name',
              'version'
            ],
            'type': u'object'
          },
          '@time': {'type': 'integer'},
          'bat': {'type': 'boolean'},
          'foo': {'type': 'string'},
          'lala': {
            'properties': {
              'haha': {'type': 'integer'}
            },
            'required': ['haha'],
            'type': 'object'}
          },
          'required': ['@id', '@library', '@time'],
          'type': 'object'
        },
        'status': 'OK'
      })
