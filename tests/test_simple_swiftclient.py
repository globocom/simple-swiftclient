import json
import unittest
from collections import namedtuple

from mock import patch, MagicMock

from simple_swiftclient.client import Client, ClientException
from simple_swiftclient.utils import list_dir


class TestSimpleSwiftClient(unittest.TestCase):

    def setUp(self,):
        self.patcher = patch('simple_swiftclient.client.urllib2.urlopen')
        self.mock_urlopen = self.patcher.start()
        self.mock_urlopen.return_value.read.return_value = '{"access": {"token": {"issued_at": "2014-12-05T20:32:34.628326", "expires": "2014-12-05T21:32:34Z", "id": "1234", "tenant": {"description": "Tenant descr", "enabled": true, "id": "1234", "name": "tenant_name"}}, "serviceCatalog": [{"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "http://internalurl/", "id": "1234", "publicURL": "http://publicurl/"}], "endpoints_links": [], "type": "object-store", "name": "swift"}, {"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "https://internalurl/v1/AUTH_12345", "id": "1234", "publicURL": "https://publicurl/v1/AUTH_12345"}], "endpoints_links": [], "type": "identity", "name": "keystone"}], "user": {"username": "username", "roles_links": [], "id": "1234", "roles": [{"name": "_member_"}], "name": "User name"}, "metadata": {"is_admin": 0, "roles": ["1234"]}}}'

    def tearDown(self):
        self.patcher.stop()

    def test_should_return_a_token(self):
        cli = Client({})
        self.assertEqual(cli.get_token(), '1234')

    @patch('simple_swiftclient.client.urllib2.urlopen')
    def test_should_return_error_if_response_is_not_json(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = '404 Not Found'
        self.assertRaises(ClientException, Client, {})

    def test_new_client_should_have_token(self):
        cli = Client({})
        self.assertIsNotNone(cli.get_token())

    @patch('simple_swiftclient.client.urllib2.Request')
    def test_nelson_de_um_nome(self, mock_request):
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

        self.mock_urlopen.assert_called_once_with(request_object)

    @patch('simple_swiftclient.client.urllib2.Request')
    def test_get_token_builds_request_correctly(self, mock_request):
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

    def test_class_init_should_authenticate(self):

        cli = Client({})

        expected = {
            'token': json.loads('{"issued_at": "2014-12-05T20:32:34.628326", "expires": "2014-12-05T21:32:34Z", "id": "1234", "tenant": {"description": "Tenant descr", "enabled": true, "id": "1234", "name": "tenant_name"}}'),
            'service_catalog': json.loads('[{"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "http://internalurl/", "id": "1234", "publicURL": "http://publicurl/"}], "endpoints_links": [], "type": "object-store", "name": "swift"}, {"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "https://internalurl/v1/AUTH_12345", "id": "1234", "publicURL": "https://publicurl/v1/AUTH_12345"}], "endpoints_links": [], "type": "identity", "name": "keystone"}]'),
            'user': json.loads('{"username": "username", "roles_links": [], "id": "1234", "roles": [{"name": "_member_"}], "name": "User name"}'),
            'metadata': json.loads('{"is_admin": 0, "roles": ["1234"]}'),
        }

        self.assertEqual(cli._token, expected.get('token'))
        self.assertEqual(cli._service_catalog, expected.get('service_catalog'))
        self.assertEqual(cli._user, expected.get('user'))
        self.assertEqual(cli._metadata, expected.get('metadata'))

    def test_should_return_adminurl(self):
        cli = Client({})

        self.assertEqual(cli.get_storage_url(), 'https://adminurl/v1/AUTH_12345')

    @patch('simple_swiftclient.client.urllib2.Request')
    @patch('simple_swiftclient.utils.list_dir')
    @patch('simple_swiftclient.client.Client._authenticate')
    def test_upload_should_build_request_correctly(self, mock__authenticate, mock_list_dir, mock_request):
        mock_list_dir.return_value = ['image.jpg']

        cli = Client({})
        cli._token = json.loads('{"issuedat": "2014-12-05T20:32:34.628326", "expires": "2014-12-05T21:32:34Z", "id": "1234", "tenant": {"description": "Tenant descr", "enabled": true, "id": "1234", "name": "tenant_name"}}')
        cli._service_catalog = json.loads('[{"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "http://internalurl/", "id": "1234", "publicURL": "http://publicurl/"}], "endpoints_links": [], "type": "object-store", "name": "swift"}, {"endpoints": [{"adminURL": "https://adminurl/v1/AUTH_12345", "region": "RegionOne", "internalURL": "https://internalurl/v1/AUTH_12345", "id": "1234", "publicURL": "https://publicurl/v1/AUTH_12345"}], "endpoints_links": [], "type": "identity", "name": "keystone"}]')

        cli.upload('container', 'tests/fixtures/', False)

        expected_url = "https://adminurl/v1/AUTH_12345/container/image.jpg"
        expected_headers = {
            'Content-Type': 'image/jpeg',
            'X-Storage-Token': '1234',
            'Content-Length': 77434
        }

        expected_data = open('tests/fixtures/image.jpg', 'r').read()

        mock_request.assert_called_once_with(expected_url, expected_data, expected_headers)
