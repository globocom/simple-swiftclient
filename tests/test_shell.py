import unittest
import os

from mock import patch

from simple_swiftclient import shell


class TestShell(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('simple_swiftclient.shell.st_upload')
    def test_upload_subcommand_calls_upload_method(self, mock_upload):

        sys_argv = ['/path/to/script',
            '--os-auth-url', 'https://localhost:5000/v2.0',
            '--os-username', 'usuario',
            '--os-password', 'senha',
            '--os-tenant-name', 'infra',
            '--os-storage-url', 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603',
            'upload', 'a3d1e5', 'service.py']

        shell.main(sys_argv)
        self.assertTrue(mock_upload.called)

        _, _, kargs = mock_upload.mock_calls[0]

        options = kargs.get('options')

        expected = {
            'os_username': 'usuario',
            'os_password': 'senha',
            'os_auth_url': 'https://localhost:5000/v2.0',
            'os_tenant_name': 'infra',
            'os_storage_url': 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603'
        }

        self.assertEqual(expected.get('os_username'), options.os_username)
        self.assertEqual(expected.get('os_password'), options.os_password)
        self.assertEqual(expected.get('os_auth_url'), options.os_auth_url)
        self.assertEqual(expected.get('os_tenant_name'), options.os_tenant_name)
        self.assertEqual(expected.get('os_storage_url'), options.os_storage_url)

    @patch('simple_swiftclient.shell.st_upload')
    def test_upload_subcommand_reading_env_variables(self, mock_upload):
        os.environ['OS_USERNAME'] = 'user_env'
        os.environ['OS_PASSWORD'] = 'password_env'
        os.environ['OS_AUTH_URL'] = 'https://localhost:5000/v2.0_env'
        os.environ['OS_TENANT_NAME'] = 'infra_env'
        os.environ['OS_STORAGE_URL'] = 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603_env'
        sys_argv = ['/path/to/script', 'upload', 'a3d1e5', 'service.py']

        shell.main(sys_argv)
        self.assertTrue(mock_upload.called)

        _, _, kargs = mock_upload.mock_calls[0]

        options = kargs.get('options')

        expected = {
            'os_username': 'user_env',
            'os_password': 'password_env',
            'os_auth_url': 'https://localhost:5000/v2.0_env',
            'os_tenant_name': 'infra_env',
            'os_storage_url': 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603_env'
        }

        self.assertEqual(expected.get('os_username'), options.os_username)
        self.assertEqual(expected.get('os_password'), options.os_password)
        self.assertEqual(expected.get('os_auth_url'), options.os_auth_url)
        self.assertEqual(expected.get('os_tenant_name'), options.os_tenant_name)
        self.assertEqual(expected.get('os_storage_url'), options.os_storage_url)

        del os.environ['OS_USERNAME']
        del os.environ['OS_PASSWORD']
        del os.environ['OS_AUTH_URL']
        del os.environ['OS_TENANT_NAME']
        del os.environ['OS_STORAGE_URL']

    @patch('simple_swiftclient.shell.st_upload')
    def test_upload_subcommand_reading_swiftsuru_variables(self, mock_upload):
        os.environ['SWIFT_USER'] = 'user_swiftsuru'
        os.environ['SWIFT_PASSWORD'] = 'password_swiftsuru'
        os.environ['SWIFT_AUTH_URL'] = 'https://localhost:5000/v2.0_swiftsuru'
        os.environ['SWIFT_TENANT'] = 'infra_swiftsuru'
        os.environ['SWIFT_ADMIN_URL'] = 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603_swiftsuru'
        sys_argv = ['/path/to/script', 'upload', 'a3d1e5', 'service.py']

        shell.main(sys_argv)
        self.assertTrue(mock_upload.called)

        _, _, kargs = mock_upload.mock_calls[0]

        options = kargs.get('options')

        expected = {
            'os_username': 'user_swiftsuru',
            'os_password': 'password_swiftsuru',
            'os_auth_url': 'https://localhost:5000/v2.0_swiftsuru',
            'os_tenant_name': 'infra_swiftsuru',
            'os_storage_url': 'https://localhost/v1/AUTH_f3337981c3734eb297239ead9f295603_swiftsuru'
        }

        self.assertEqual(expected.get('os_username'), options.os_username)
        self.assertEqual(expected.get('os_password'), options.os_password)
        self.assertEqual(expected.get('os_auth_url'), options.os_auth_url)
        self.assertEqual(expected.get('os_tenant_name'), options.os_tenant_name)
        self.assertEqual(expected.get('os_storage_url'), options.os_storage_url)
