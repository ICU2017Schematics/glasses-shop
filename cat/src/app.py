"""Product Catalog service for eyeglasses example"""
import os
import json
from flask import Flask, request, abort
from flask_cors import CORS
from cloudant.client import Cloudant
from cloudant.query import Query

# Cloudant setup
USER = os.getenv('CLOUDANT_USER', '1d5b1d71-6725-479a-9d02-960a9696d4dc-bluemix')
PASS = os.getenv('CLOUDANT_PASS', 'f34918ec19b92a8fa07f5012ee8d3f4ee0ffc0b2c363ccc559f0920340c8bfcb')
URL  = os.getenv('CLOUDANT_URL', 'https://1d5b1d71-6725-479a-9d02-960a9696d4dc-bluemix.cloudant.com')
client = Cloudant(USER, PASS, url=URL, connect=True, auto_renew=True)

# ----- Flask setup
app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'OUR LITTLE SECRET'
CORS(app)

# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def query(field, value):
    body = list()
    collection = client['products']
    f = field

    query = Query(collection, selector={f: {'$eq': value}})
    docs = list()
    for doc in query()['docs']:
        docs.append(doc)
    
    for product in docs:
        product['percent_savings'] = 100.0 * (1.0 - float(product['sale_price']) / float(product['retail_price']))
        body.append(product)

    return json.dumps(body, sort_keys=True, skipkeys=True, indent=4), 200

# ----- route handlers

@app.before_request
def before_request():
    if 'health' not in request.url and not request_wants_json():
        abort(415)

@app.route('/cat', methods=['GET'])
def home():
    body = list()
    collection = client['categories']
    for doc in collection:
        body.append(doc)

    response_json = json.dumps(body, sort_keys=True, skipkeys=True, indent=4)
    return response_json, 200

@app.route('/cat/products', methods=['GET'])
def get_products():
    body = list()
    collection = client['products']
    if 'gender' in request.args:
        response_json, sc = query('category1', request.args['gender'])
    elif 'rim' in request.args:
        response_json, sc = query('category2', request.args['rim'])
    elif 'shape' in request.args:
        response_json, sc = query('category3', request.args['shape'])
    elif 'material' in request.args:
        response_json, sc = query('category4', request.args['material'])
    else:
        for product in collection:
            body.append(product)
        response_json = json.dumps(body, sort_keys=True, skipkeys=True, indent=4)
        sc = 200

    return response_json, sc

@app.route('/cat/products/<id>', methods=['GET'])
def get_product(id):
    collection = client['products']
    query = Query(collection, selector={'product_id': {'$eq': id}})
    body = {}
    for doc in query()['docs']:
        body = doc

    response_json = json.dumps(body, sort_keys=True, skipkeys=True, indent=4)
    return response_json, 200

@app.route('/cat/__health__', methods=['GET'])
def healthcheck():
    return '1'

if __name__ == '__main__':
    PORT = os.getenv('VCAP_APP_PORT', '5000')
    app.debug = os.getenv('DEBUG', False)
    app.run(host='0.0.0.0', port=int(PORT), threaded=True)
