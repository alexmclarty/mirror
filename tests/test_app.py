from flask import json

import app
import unittest


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_post_returns_200(self):

        payload = {
            "endpoint": "/post_test",
            "methods": ["POST"],
            "status_code": 200,
            "json_response": {}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.post('/post_test')
        assert response.status_code == 200

    def test_get_returns_200(self):

        payload = {
            "endpoint": "/cheese",
            "methods": ["GET"],
            "status_code": 200,
            "json_response": {}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.get('/cheese')
        assert response.status_code == 200

    def test_get_returns_json(self):

        payload = {
            "endpoint": "/json_test",
            "methods": ["GET"],
            "status_code": 200,
            "json_response": {'cheese_flavour': 'cheddar'}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.get('/json_test')
        assert response.status_code == 200
        json_response = json.loads(response.data)
        assert json_response['cheese_flavour']

    def test_non_standard_status_code(self):

        payload = {
            "endpoint": "/non_standard",
            "methods": ["GET"],
            "status_code": 300,
            "json_response": {'cheese_flavour': 'cheddar'}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.get('/non_standard')
        assert response.status_code == 300

    def test_update_endpoint(self):

        # Setup endpoint
        payload = {
            "endpoint": "/endpoint_to_update",
            "methods": ["GET"],
            "status_code": 200,
            "json_response": {'cheese_flavour': 'cheddar'}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.get('/endpoint_to_update')
        assert response.json['cheese_flavour'] == 'cheddar'
        assert response.status_code == 200

        # Setup endpoint with a different response
        payload = {
            "endpoint": "/endpoint_to_update",
            "methods": ["GET"],
            "status_code": 200,
            "json_response": {'cheese_flavour': 'gouda'}
        }

        json_payload = json.dumps(payload)

        self.app.post('/register', data=json_payload, headers={'content-type': 'application/json'})

        response = self.app.get('/endpoint_to_update')
        assert response.status_code == 200
        assert response.json['cheese_flavour'] == 'gouda'

    def test_get_code(self):
        response = self.app.get('/get_code')
        assert response.status_code == 200

    def test_get_token(self):
        response = self.app.post('/connect/token')
        assert response.status_code == 200
        json_response = json.loads(response.data)
        assert json_response['id_token']

    def test_get_key(self):
        response = self.app.get('/get_key')
        assert response.status_code == 200
        json_response = json.loads(response.data)
        assert json_response['keys']


if __name__ == '__main__':
    unittest.main()
