import urllib2
import json


class ClientException(Exception):
    pass

class Client(object):

    def __init__(self, opts):
        self.auth_url = opts.get('auth_url')
        self.username = opts.get('username')
        self.password = opts.get('password')
        self.tenant_name = opts.get('tenant_name')

        self.token = self.get_token()

    def get_token(self):

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
            token = json_resp['access']['token']['id']
        except ValueError:
            raise ClientException('')

        conn.close()

        return token

