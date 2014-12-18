import os

DEBUG = True
PORT = 9192

# All enabled executors.
EXECUTORS = [
  'metis.core.execute.python.PythonExecutor',
  'metis.core.execute.spark.SparkExecutor',
]

# The default executor to use, if none is specified in the request.
DEFAULT_EXECUTOR = 'metis.core.execute.python.PythonExecutor'

# A list of the data sources available to query
DATA_SOURCES = {
  'kronos': {  # A meaningful name... can be anything
    'type': 'metis.core.query.kronos.source.KronosSource',
    'pretty_name': 'Kronos',  # Displayed to the user
    'url': 'http://localhost:9191',  # Kronos server URL
  },
}

DATA_SOURCE_ADAPTERS = [
  'metis.core.query.kronos.adapters.Python',
  'metis.core.query.kronos.adapters.Spark',
]

# Location of Spark home, where we can find PySpark.
# Set SPARK_HOME env variable before running tests. If you are lazy, symlink
# it in your home directory.
SPARK_HOME = os.environ.get('SPARK_HOME',
                            '%s/spark-1.0.0' % os.environ.get('HOME'))

# Host name of the master node of your Spark cluster.
SPARK_MASTER = 'local'
