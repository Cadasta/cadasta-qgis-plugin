# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

import os
import qgis
import logging
from cadasta.api.login import Login
from qgis.PyQt.QtCore import QCoreApplication

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class LoginTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.url = 'https://demo.cadasta.org/'
        self.username = 'kartoza.demo'
        self.password = 'demo.kartoza1!'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_login(self):
        """Test we can click OK."""
        login = Login(self.url, self.username, self.password)
        # Wait until it finished
        while not login.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(login.get_json_results())


if __name__ == "__main__":
    suite = unittest.makeSuite(LoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
