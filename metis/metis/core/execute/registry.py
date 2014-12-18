from importlib import import_module
from metis import app


class DataSourceAdapterRegistry(object):
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(DataSourceAdapterRegistry, cls).__new__(cls, *args,
                                                                    **kwargs)
    return cls._instance

  def __init__(self):
    self._data_source_adapters = {}

    for operator in app.config['DATA_SOURCE_ADAPTERS']:
      op_module, op_cls = operator.rsplit('.', 1)
      op_module = import_module(op_module)
      op_cls = getattr(op_module, op_cls)
      self.register(op_cls)

  def register(self, data_source_adapter):
    pair = data_source_adapter.executor_source_pair()
    self._data_source_adapters[pair] = data_source_adapter

  def get(self, executor, data_source):
    return self._data_source_adapters.get((executor, data_source))

