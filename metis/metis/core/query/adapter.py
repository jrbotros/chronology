class DataSourceAdapter(object):
  @classmethod
  def executor_source_pair(self):
    raise NotImplemented

  def execute(self, node, executor):
    raise NotImplemented


