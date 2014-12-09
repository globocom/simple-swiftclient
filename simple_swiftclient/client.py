from __future__ import print_function

import json
import urllib2

import utils


class ClientException(Exception):
    pass


class Client(object):

    def __init__(self, opts):
        self.auth_url = opts.get('auth_url')
        self.username = opts.get('username')
        self.password = opts.get('password')
        self.tenant_name = opts.get('tenant_name')

        self._token = None
        self._service_catalog = None
        self._user = None
        self._metadata = None

        self._authenticate()

    def _authenticate(self):

        data = json.dumps({
            "auth": {
                "tenantName": self.tenant_name,
                "passwordCredentials": {
                    "username": self.username,
                    "password": self.password
                }
            }
        })

        url = '{}/tokens'.format(self.auth_url)

        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        conn = urllib2.urlopen(req)
        resp = conn.read()

        try:
            json_resp = json.loads(resp)
        except ValueError:
            raise ClientException('Fail to authenticate')

        conn.close()

        self._token = json_resp.get('access').get('token')
        self._service_catalog = json_resp.get('access').get('serviceCatalog')
        self._user = json_resp.get('access').get('user')
        self._metadata = json_resp.get('access').get('metadata')

    def get_token(self):
        return self._token.get('id')

    def get_storage_url(self):
        for service in self._service_catalog:
            if service.get('type') == 'object-store':
                endpoints = service.get('endpoints')
                return endpoints[0].get('adminURL')

        raise ClientException('No endpoint found!')

    def upload(self, container, path, verbose=True):
        if path[-1] == '/':
            path = path[:-1]

        import ipdb;ipdb.set_trace()
        files = utils.list_dir(path)

        for filename in files:

            (fh, content_type, content_length) = utils.get_file_infos(filename)

            url = "{}/{}/{}".format(self.get_storage_url(),
                                    container,
                                    filename)

            data = fh.read()

            headers = {
                'Content-Type': content_type,
                'X-Storage-Token': self.get_token(),
                'Content-Length': content_length
            }

            request = urllib2.Request(url, data, headers)
            request.get_method = lambda: 'PUT'

            response = urllib2.urlopen(request)

            if response.code == 201:
                msg = '{} - OK'.format(filename)
            else:
                msg = '{} - FAIL (error {})'.format(filename, response.code)

            if verbose:
                print(msg)
