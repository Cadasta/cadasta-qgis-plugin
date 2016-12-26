# coding=utf-8

"""Tests for login api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

from qgis.PyQt.QtCore import QCoreApplication
from mock.mock import MagicMock
from mock import patch
from cadasta.api.login import Login


class LoginTest(unittest.TestCase):
    """Test dialog works."""

    login_result = {
        'auth_token': 'dasdsa327142h3j41j'
    }

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

    @patch("cadasta.api.login.Login.__init__")
    def test_login(self, mock_init):
        """Test we can click OK."""
        mock_init.return_value = None
        organization_project = Login()
        organization_project.get_json_results = MagicMock(
            return_value=(True, self.login_result)
        )
        results = organization_project.get_json_results()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], dict)


if __name__ == "__main__":
    suite = unittest.makeSuite(LoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
