# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

from source.api.login import Login
from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class LoginTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.username = 'irwan.kartoza'
        self.password = 'Irwankartoza1!'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_login(self):
        """Test we can click OK."""
        Login(self.username, self.password)


if __name__ == "__main__":
    suite = unittest.makeSuite(LoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
