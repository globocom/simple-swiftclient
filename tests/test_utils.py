import os
import shutil
import unittest

from simple_swiftclient import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        TestUtils._make_tmp_dir()

    def tearDown(self):
        TestUtils._delete_tmp_dir()

    @staticmethod
    def _make_tmp_dir():
        base_path = '/tmp/teste-swiftclient-tmp-dir'

        os.makedirs('{}/dir01/dir0101'.format(base_path))
        fh = open('{}/dir01/dir0101/file01'.format(base_path), 'a')
        fh.write('um arquivo aleatorio')
        fh.close()

        os.makedirs('{}/dir02'.format(base_path))
        open('{}/dir02/file02'.format(base_path), 'a').close()

        os.makedirs('{}/dir03'.format(base_path))

    @staticmethod
    def _delete_tmp_dir():
        shutil.rmtree('/tmp/teste-swiftclient-tmp-dir')

    def test_should_return_a_list_with_all_files_in_a_directory(self):

        expected = [
            '/tmp/teste-swiftclient-tmp-dir/dir01/dir0101/file01',
            '/tmp/teste-swiftclient-tmp-dir/dir02/file02',
        ]

        computed = utils.list_dir('/tmp/teste-swiftclient-tmp-dir')

        self.assertEqual(computed, expected)

    def test_should_return_a_list_with_one_file(self):

        expected = [
            '/tmp/teste-swiftclient-tmp-dir/dir01/dir0101/file01',
        ]

        computed = utils.list_dir('/tmp/teste-swiftclient-tmp-dir/dir01/dir0101/file01')

        self.assertEqual(computed, expected)

    def test_list_dir_should_return_a_empty_list_for_an_empty_dir(self):
        computed = utils.list_dir('/tmp/teste-swiftclient-tmp-dir/dir03')
        self.assertEqual(computed, [])

    def test_get_infos_of_a_file(self):

        filename = 'tests/fixtures/image.jpg'
        (fh, content_type, content_length) = utils.get_file_infos(filename)

        self. assertEqual('image/jpeg', content_type)
        self. assertEqual(77434, content_length)

        expected_str_fh = "<open file 'tests/fixtures/image.jpg'"
        self.assertIn(expected_str_fh, str(fh))
