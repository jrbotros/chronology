import json

from flask import jsonify
from flask import request
from flask import Response

import metis

from metis import app
from metis.core.execute.service import service
from metis.core.query.operator import DataAccess

@app.route('/1.0/index', methods=['GET'])
def index():
  return jsonify({
      'status': 'metisd',
      'version': metis.get_version()
  })


@app.route('/1.0/sources', methods=['GET'])
def data_sources():
  response = {'status': 'OK',
              'sources': {}}
  for source, source_info in app.config['DATA_SOURCES'].iteritems():
    response['sources'][source] = {
      'type': source_info['type'],
      'pretty_name': source_info['pretty_name']}
  return jsonify(response)


@app.route('/1.0/streams/<source_name>')
def get_streams(source_name):
  source = DataAccess.parse({ 'source': source_name })
  streams = source.get_streams()
  response_dict = {
    'streams': streams,
    'status': 'OK',
  }
  return jsonify(response_dict)


@app.route('/1.0/streams/<source_name>/<stream_name>')
def get_schema(source_name, stream_name):
  source = DataAccess.parse({ 'source': source_name })
  schema = source.get_schema(stream_name)
  response_dict = {
    'schema': schema['schema'],
    'status': 'OK',
  }
  return jsonify(response_dict)


# TODO(usmanm): Add error handling everywhere.
@app.route('/1.0/query', methods=['POST'])
def query():
  # TODO(usmanm): `force` doesn't seem to work. Still need to send the correct
  # application/json header.
  request_json = request.get_json(force=True)
  events = service.execute_plan(request_json['plan'],
                                request_json.get('executor'))
  return Response(('%s\r\n' % json.dumps(event) for event in events),
                  mimetype='application/json')
