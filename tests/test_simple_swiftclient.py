import json
import unittest
import urllib2
from collections import namedtuple

from mock import patch

from simple_swiftclient.client import Client, ClientException


class TestSimpleSwiftClient(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('simple_swiftclient.client.urllib2.urlopen')
    def test_should_return_a_token(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = '{"access": {"token": {"id": "123"}}}'
        cli = Client({})
        self.assertEqual(cli.get_token(), '123')

    @patch('simple_swiftclient.client.urllib2.urlopen')
    def test_should_return_error_if_response_is_not_json(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = '404 Not Found'
        self.assertRaises(ClientException, Client, {})

    @patch('simple_swiftclient.client.Client.get_token')
    def test_new_client_should_have_token(self, mock_get_token):

        Client({})
        self.assertTrue(mock_get_token.called)

    @patch('simple_swiftclient.client.urllib2.Request')
    @patch('simple_swiftclient.client.urllib2.urlopen')
    def test_nelson_de_um_nome(self, mock_urlopen, mock_request):
        mock_urlopen.return_value.read.return_value = '{"access": {"token": {"id": "123"}}}'
        opts = {
            'username': 'usuario',
            'password': 'senha',
            'auth_url': 'http://localhost',
            'tenant_name': 'my_tenant',
        }

        data = json.dumps({
            "auth": {
                "tenantName": opts.get('tenant_name'),
                "passwordCredentials": {
                    "username": opts.get('username'),
                    "password": opts.get('password')
                }
            }
        })

        request_object = namedtuple("Request", ["url", "data", "headers"])(opts["auth_url"], data, {'Content-Type': 'application/json'})
        mock_request.return_value = request_object

        Client(opts)

        mock_urlopen.assert_called_once_with(request_object)

    @patch('simple_swiftclient.client.urllib2.Request')
    @patch('simple_swiftclient.client.urllib2.urlopen')
    def test_get_token_builds_request_correctly(self, mock_urlopen, mock_request):
        mock_urlopen.return_value.read.return_value = '{"access": {"token": {"id": "123"}}}'
        opts = {
            'username': 'usuario',
            'password': 'senha',
            'auth_url': 'http://localhost',
            'tenant_name': 'my_tenant',
        }
        fake_data = json.dumps({
            "auth": {
                "tenantName": opts.get('tenant_name'),
                "passwordCredentials": {
                    "username": opts.get('username'),
                    "password": opts.get('password')
                }
            }
        })

        Client(opts)

        mock_request.assert_called_once_with("http://localhost/tokens", fake_data, {'Content-Type': 'application/json'})



