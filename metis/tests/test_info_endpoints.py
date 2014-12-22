from tests.server import MetisServerTestCase


class CohortTestCase(MetisServerTestCase):

  def test_index(self):
    response = self.index()
    self.assertEquals(response, {'status': 'metisd', 'version': '0.1 alpha'})


  def test_data_sources(self):
    response = self.data_sources()
    self.assertEquals(response, {'status': 'OK', 'sources': {
      'kronos': {'pretty_name': 'Kronos',
                 'type': 'metis.core.query.kronos.source.KronosSource'}}})
