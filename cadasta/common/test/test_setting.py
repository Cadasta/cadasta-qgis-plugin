# coding=utf-8
"""Tests for setting.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import unittest

import os
from cadasta.common.setting import (
    delete_authtoken,
    delete_setting,
    delete_url_instance,
    get_authtoken,
    get_setting,
    get_url_instance,
    save_authtoken,
    set_setting,
    save_url_instance,
    default_domain
)

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class SettingTest(unittest.TestCase):
    """Test setting utilities."""

    def setUp(self):
        """Runs before each test."""
        self.authtoken = "test_token"
        self.url = "http://test.com/"

    def tearDown(self):
        """Runs after each test."""

    def test_set_setting(self):
        """Test set setting."""
        set_setting('test_key', 'test_value')
        self.assertEqual('test_value', get_setting('test_key'))

    def test_get_setting(self):
        """Test get setting."""
        set_setting('test_key', None)
        self.assertIsNone(get_setting('test_key'))

    def test_delete_setting(self):
        """Test delete setting."""
        set_setting('test_key', 'test_value')
        self.assertEqual('test_value', get_setting('test_key'))

        delete_setting('test_key')
        self.assertIsNone(get_setting('test_key'))

    def test_save_authtoken(self):
        """Test save authtoken."""
        save_authtoken(self.authtoken)
        self.assertEqual(self.authtoken, get_authtoken())

    def test_delete_authtoken(self):
        """Test delete authtoken."""
        save_authtoken(self.authtoken)
        self.assertEqual(self.authtoken, get_authtoken())

        delete_authtoken()
        self.assertIsNone(get_authtoken())

    def test_save_url_instance(self):
        """Test save url instance."""
        save_url_instance(self.url)
        self.assertEqual(self.url, get_url_instance())

    def test_delete_url_instance(self):
        """Test delete url instance."""
        save_url_instance(self.url)
        self.assertEqual(self.url, get_url_instance())

        delete_url_instance()
        self.assertEqual(default_domain, get_url_instance())


if __name__ == "__main__":
    suite = unittest.makeSuite(SettingTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
