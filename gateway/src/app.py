"""API Gateway"""
import os
import uuid
import json
import requests
from flask import Flask, request, redirect, session, abort
from flask_cors import CORS

CART_ENTRYPOINT = os.environ['CART_ENTRYPOINT'] if 'CART_ENTRYPOINT' in os.environ else ''
CAT_ENTRYPOINT = os.environ['CAT_ENTRYPOINT'] if 'CAT_ENTRYPOINT' in os.environ else ''
SHIP_ENTRYPOINT = os.environ['SHIP_ENTRYPOINT'] if 'SHIP_ENTRYPOINT' in os.environ else ''

# ----- Flask setup
app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'OUR LITTLE SECRET'
CORS(app)

headers = {'Accept': 'application/json'}

# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    if request.method == 'OPTIONS':
        return True

    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

@app.before_request
def before_request():
    if 'session-id' not in session:
        session['session-id'] = uuid.uuid4()

    if 'health' not in request.url and 'orders' not in request.url:
        if not request_wants_json():
            abort(415)

@app.route('/', methods=['GET'])
def home():
    r = requests.get(CAT_ENTRYPOINT + '/cat', headers=headers)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/cart/<id>', methods=['GET'])
def cart(id):
    rh = headers
    r = requests.get(CART_ENTRYPOINT + '/' + id, headers=rh)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/cart/<id>', methods=['POST'])
def add_to_cart(id):
    rh = headers
    rh['X-Cart-Token'] = request.headers.get('X-Cart-Token')

    data = {}
    data['lineitem'] = request.json['lineitem']

    r = requests.post(CART_ENTRYPOINT + '/' + id, headers=rh, json=data)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 201

@app.route('/cart/<id>', methods=['DELETE'])
def delete_cart(id):
    rh = headers
    rh['X-Cart-Token'] = request.headers.get('X-Cart-Token')

    r = requests.delete(CART_ENTRYPOINT + '/' + id, headers=rh)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/orders', methods=['POST'])
def post_order():
    rh = headers
    rh['Content-Type'] = 'application/json'

    data = {}
    data['order'] = request.json['order']

    r = requests.post(SHIP_ENTRYPOINT + '/api/orders', headers=rh, json=data)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 201

@app.route('/products', methods=['GET'])
def get_products():
    r = requests.get(CAT_ENTRYPOINT + '/cat/products', headers=headers, params = request.args)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    r = requests.get(CAT_ENTRYPOINT + '/cat/products/' + id, headers=headers, params = request.args)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/categories', methods=['GET'])
def get_cats():
    r = requests.get(CAT_ENTRYPOINT + '/cat/categories', headers=headers, params = request.args)
    if r.status_code != 200 and r.status_code != 201:
        abort(r.status_code)

    response_json = r.text
    return response_json, 200

@app.route('/__health__', methods=['GET'])
def healthcheck():
    return '1'

if __name__ == '__main__':
    PORT = os.getenv('VCAP_APP_PORT', '5000')
    app.debug = os.getenv('DEBUG', False)
    app.run(host='0.0.0.0', port=int(PORT), threaded=True)
