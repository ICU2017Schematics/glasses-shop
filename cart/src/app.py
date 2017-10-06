"""Shopping Cart as a Service"""
import os
import json
import time
import uuid
from flask import Flask, Response, abort, request
from flask_cors import CORS

# for now we'll make the carts an in-memory list
carts = {}

# ----- Flask setup
app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'OUR LITTLE SECRET'
CORS(app)

def is_admin(authorization): 
    return True

def validate_cart(id, cart_token):
    return True if id in carts and carts[id]['cart_token'] == cart_token else False

def generate_cart_token():
    return str(uuid.uuid4())

def create_cart(id):
    carts[id] = {}
    carts[id]['created'] = int(time.time())
    carts[id]['cart_token'] = generate_cart_token()
    carts[id]['lineitems'] = {}

@app.route('/', methods=['GET'])
def get_carts():
    if 'authorization' not in request.headers:
        abort(403)
    if not is_admin(request.headers['authorization']):
        abort(403)

    response = Response(json.dumps(carts))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response
  
@app.route('/<id>', methods=['POST'])
def add_to_cart(id):
    if not request.json or not 'lineitem' in request.json:
        abort(400)

    cart_token = request.headers.get('X-Cart-Token')
    if not validate_cart(id, cart_token):
        abort(403)

    if id not in carts:
        create_cart(id)

    cart = carts[id]
    lineitems = cart['lineitems']

    lineitem = request.json['lineitem']
    product_id = lineitem['product_id']
    if product_id in lineitems:
        lineitems[product_id]['qty'] += 1
    else:
        lineitems[product_id] = lineitem
        lineitems[product_id]['qty'] = 1

    response = Response(json.dumps(cart))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 201
    return response

@app.route('/<id>', methods=['PUT'])
def replace_cart(id):
    if id not in carts:
        abort(404)
    if 'cart' not in request.json:
        abort(401)

    cart = carts[id]
    cart['lineitems'].pop()
    cart['lineitems'] = request.json['cart']

    response = Response(json.dumps(cart))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 201
    return response

@app.route('/<id>', methods=['GET'])
def get_cart(id):
    if id not in carts:
        create_cart(id)

    cart = carts[id]
    response = Response(json.dumps(cart))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response

@app.route('/<id>', methods=['DELETE'])
def delete_cart(id):
    if id not in carts:
        abort(404)

    cart_token = request.headers.get('X-Cart-Token')
    if not validate_cart(id, cart_token):
        abort(403)

    carts.pop(id)
    response = Response()
    response.status_code = 200
    return response

@app.route('/__health__', methods=['GET'])
def healthcheck():
    return '1'

if __name__ == '__main__':
    PORT = os.getenv('VCAP_APP_PORT', '5000')
    app.debug = os.getenv('DEBUG', False)
    app.run(host='0.0.0.0', port=int(PORT), threaded=True)
