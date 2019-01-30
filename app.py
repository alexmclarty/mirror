import sys
import uuid
import time

import os

import jwt
from flask import Flask, request, Response, jsonify, json

app = Flask(__name__)
app.logger.info("Starting app...")

# Read JWKs.
dir_path = os.path.dirname(os.path.realpath(__file__))
keypair = open('{}/keys/jwk/keypair'.format(dir_path), 'r').read()
keypair_set = open('{}/keys/jwk/keypair_set'.format(dir_path), 'r').read()
public_key = open('{}/keys/jwk/public_key'.format(dir_path), 'r').read()
private_key_pem = open('{}/keys/jwk/private_key_pem'.format(dir_path), 'r').read()

# Generate a fake token.
fake_sso_token = str(uuid.uuid4())


@app.route('/register', methods=['POST'])
def register():
    """
    Register an endpoint.
    """
    app.logger.info(request)
    parsed_json = request.get_json()

    endpoint = parsed_json['endpoint']
    methods = parsed_json['methods']
    status_code = parsed_json['status_code']
    # TODO headers = parsed_json['headers']
    json_response = parsed_json['json_response']

    for rule in app.url_map.iter_rules():
        if rule.rule == endpoint:
            # Accessing private isn't nice. Raise PR with Werkzeug to support deleting endpoints?
            app.url_map._rules.remove(rule)

    def func():
        response = jsonify(json_response)
        response.status_code = status_code
        response.headers = {'content-type': 'application/json'}
        return response

    app.add_url_rule(endpoint, str(uuid.uuid4()), view_func=func, methods=methods)
    app.logger.info("Added endpoint.")

    return Response()


@app.route('/list', methods=['GET'])
def list_routes():
    """
    List all endpoints.
    """
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


@app.route('/shutdown')
def shutdown():
    """
    Shutdown the app.
    """
    app.logger.info("Shutting down.")
    sys.exit()


# Open ID Connect

@app.route('/get_code')
def get_code():
    """
    Returns a fake code.
    :return:
    """
    return jsonify({'code': fake_sso_token})


@app.route('/connect/token', methods=['POST'])
def get_token():
    """
    {
        u'access_token': u'eyJhbGciOiJS...',
        u'id_token': u'eyJhbGciOiJSUzI1...',
        u'expires_in': 3600,
        u'refresh_token': u'1dade9e9416...',
        u'token_type': u'Bearer'
    }
    :return:
    """
    now = int(time.time())
    jwt_payload = {
        u'family_name': u'Test User',
        u'aud': u'test',
        u'iss': u'http://mirror',
        u'auth_time': now,
        u'idp': u'local',
        u'name': u'',
        u'at_hash': u'DgCSE3R2ZN03RQeXuYZTkw',
        u'email': u'test@example.com',
        u'given_name': u'gtv2super',
        u'exp': now + 600,  # Add 10 minutes onto the current time.
        u'sid': u'b160650a57dd1db6d5af38f7f90d25e3',
        u'iat': now,
        u'amr': [u'pwd'],
        u'nickname': u'test_user',
        u'nbf': 1511535122,
        u'sub': u'e463d3c8-42e8-41f7-835b-87c0f722fe4e'
    }

    id_token = jwt.encode(jwt_payload, private_key_pem, algorithm='RS256')

    token_exchange_payload = {
        "id_token": id_token.decode('utf-8'),
        "access_token": str(uuid.uuid4()),
        "expires_in": 3600,
        "token_type": "Bearer",
        "refresh_token": str(uuid.uuid4())
    }

    return jsonify(token_exchange_payload)


@app.route('/get_key')
def get_key():
    """
    Return the public JWK in JWKS format.
    :return: response
    """
    public_key_dict = json.loads(public_key)
    return jsonify({
        'keys': [
            public_key_dict
        ]
    })

if __name__ == '__main__':
    ssl_context = None
    if os.getenv('USE_SSL', False):
        ssl_context = "adhoc"

    app.run(host='0.0.0.0', port=6001, debug=os.getenv('DEBUG', False), ssl_context=ssl_context)
