import json
import requests
import time

from threading import Thread, Lock
from collections import defaultdict

from utils import kronos_time_now


class KronosClientException(Exception):
  pass


class KronosClient(object):
  """
  Initialize a Kronos client that can connect to a server at `http_url`

  Put requests are non-blocking if `blocking`=False.
  If non-blocking, `sleep_block` specifies the frequency of
    a background thread that flushes events to the server.
  """

  # These are constants, do not modify them.
  TIMESTAMP_FIELD = '@time'
  ID_FIELD = '@id'

  def __init__(self, http_url, blocking=True, sleep_block=0.1):
    self._put_url = '%s/1.0/events/put' % http_url
    self._get_url = '%s/1.0/events/get' % http_url
    self._index_url = '%s/1.0/index' % http_url
    self._streams_url = '%s/1.0/streams' % http_url
    self._blocking = blocking
    if not blocking:
      self._sleep_block = sleep_block
      self._setup_nonblocking()

  def index(self):
    return requests.get(self._index_url).json()

  def put(self, event_dict):
    """
    Sends a dictionary of `event_dict` of the form {stream_name:
    [event, ...], ...}  to the server.
    
    The `blocking` parameter allows the request to block until the
    server responds, and returns some information on the response.
    Here's an example:

    {u'stream_name_1': 3, u'stream_name_2': 1, u'@took': u'1ms'}
      -> put 3 events on stream_name_1
      -> put 1 event on stream_name_2
      -> put took 1ms to complete

    If `blocking` is false and the process running the client ends
    before flushing the pending data to the server, you might lose
    that data.  Calling `flush` will block until all pending data has
    been acknowledged by the server.
    """

    # Ensure that all events have a timestamp.
    timestamp = kronos_time_now()
    for events in event_dict.itervalues():
      for event in events:
        if KronosClient.TIMESTAMP_FIELD not in event:
          event[KronosClient.TIMESTAMP_FIELD] = timestamp

    if self._blocking:
      return self._put(event_dict)
    else:
      self._put_lock.acquire()
      self._put_queue.append(event_dict)
      self._put_lock.release()

  def get(self, stream, start_time, end_time, start_id=None, limit=None):
    """
    Queries a stream with name `stream` for all events between
    `start_time` and `end_time`.  An optional `start_id` allows the
    client to restart from a failure, specifying the last ID they
    read.  An optional `limit` also limits the maximum number of
    events returned.
    """
    stream_params = {
      'stream': stream,
      'end_time': end_time
    }
    if start_id:
      stream_params['start_id'] = start_id
    else:
      stream_params['start_time'] = start_time

    if limit is not None:
      stream_params['limit'] = limit
    
    errors = []
    last_id = None
    while True:
      try:
        response = requests.post(self._get_url,
                                 data=json.dumps(stream_params),
                                 stream=True)
        if response.status_code != requests.codes.ok:
          raise KronosClientException('Bad server response code %d' %
                                      response.status_code)
        for line in response.iter_lines():
          if line:
            event = json.loads(line)
            last_id = event[KronosClient.ID_FIELD]
            yield event
        break
      except Exception, e:
        errors.append(e)
        if len(errors) == 10:
          raise KronosClientException(errors)
        if last_id != None:
          if 'start_time' in stream_params:
            del stream_params['start_time']
          stream_params['start_id'] = last_id
        time.sleep(len(errors) * 0.1)

  def get_streams(self):
    """
    Queries the Kronos server and fetches a list of streams per backend if the 
    form of { backend: backend_name, streams: [stream1, ...] }.
    """
    response = requests.get(self._streams_url, stream=True)
    if response.status_code != requests.codes.ok:
      raise KronosClientException('Bad server response code %d' %
                                  response.status_code)
    for line in response.iter_lines():
      if line:
        yield json.loads(line)
          
  def _setup_nonblocking(self):
    self._put_queue = []
    self._put_lock = Lock()

    me = self
    class PutThread(Thread):
      def __init__(self):
        Thread.__init__(self)
        self.daemon = True
      def run(self):
        while True:
          me.flush()
          time.sleep(me._sleep_block)
    PutThread().start()

  def flush(self):
    if self._blocking:
      return
    self._put_lock.acquire()
    old_queue = None
    if self._put_queue:
      old_queue = self._put_queue
      self._put_queue = []
    self._put_lock.release()
    if old_queue:
      stream_name_to_events_map = defaultdict(list)
      for event_dict in old_queue:
        for stream_name, events in event_dict.iteritems():
          stream_name_to_events_map[stream_name].extend(events)
      self._put(stream_name_to_events_map)

  def _put(self, event_dict):
    response = requests.post(self._put_url, data=json.dumps(event_dict))
    if response.status_code != requests.codes.ok:
      raise KronosClientException('Received response code %s with errors %s' %
                                  (response.status_code,
                                   response.json().get('@errors', '')))
    response_dict = response.json()
    errors = response_dict.get('@errors')
    if errors:
      raise KronosClientException('Encountered errors %s' % errors)
    return response_dict

