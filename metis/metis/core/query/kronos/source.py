import types
from metis import app
from metis.core.query.operator import DataAccess
from metis.core.query.operator import Operator


class KronosSource(DataAccess):
  def __init__(self, source, stream, start_time, end_time, namespace=None,
               **kwargs):
    self._config = app.config['DATA_SOURCES'][source]
    self._host = self._config['url']
    self.type = Operator.Type.DATA_ACCESS
    self.source = source
    self.stream = stream
    self.start_time = start_time
    self.end_time = end_time
    self.namespace = namespace
    super(KronosSource, self).__init__(**kwargs)

  @classmethod
  def parse(cls, _dict):
    kronos_source = KronosSource(**_dict)

    # TODO(usmanm): Improve validation.
    assert isinstance(kronos_source._config, types.DictType)
    assert isinstance(kronos_source._host, types.StringTypes)
    assert isinstance(kronos_source.source, types.StringTypes)
    assert isinstance(kronos_source.stream, types.StringTypes)
    assert isinstance(kronos_source.start_time, int)
    assert isinstance(kronos_source.end_time, int)
    assert (kronos_source.namespace is None or
            isinstance(kronos_source.namespace, types.StringTypes))

    return kronos_source
