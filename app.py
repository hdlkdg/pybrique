import rest
import json
from dicttoxml import dicttoxml
from flask import Flask, make_response
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
# api = Api(app, default_mediatype='application/json')
"""
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps({'response':data}), code)
    resp.headers.extend(headers or {})
    return resp
"""

@api.representation('application/xml')
def output_xml(data, code, headers=None):
    resp = make_response(dicttoxml({'response':data}), code)
    resp.headers.extend(headers or {})
    return resp

api.add_resource(rest.InfoArtist, '/artist')

if __name__ == '__main__':
    app.run(debug=True)
