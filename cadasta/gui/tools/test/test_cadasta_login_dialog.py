# coding=utf-8
"""cadasta login test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'christian@kartoza.com'
__date__ = '2016-11-25'
__copyright__ = 'Copyright 2016, Kartoza'

import os
import unittest

from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import QCoreApplication

from cadasta.gui.tools.cadasta_login import CadastaLogin
from cadasta.common.setting import (
    get_authtoken,
    get_url_instance,
    delete_authtoken
)

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class CadastaLoginDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.url = 'https://demo.cadasta.org/'
        self.username = 'kartoza.demo'
        self.password = 'demo.kartoza1!'
        delete_authtoken()

        self.dialog = CadastaLogin()

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_warning_message(self):
        """Test warning message bar shows up if username/password is empty"""
        button = self.dialog.test_connection_button
        button.click()
        message_bar = self.dialog.message_bar
        self.assertIsInstance(message_bar, QgsMessageBar)

    def test_connection_fail(self):
        """Test for failed test connection"""
        self.dialog.url_input.setText(self.url)
        self.dialog.username_input.setText('test')
        self.dialog.password_input.setText('test')
        button = self.dialog.test_connection_button
        button.click()

        while not self.dialog.login_api.reply.isFinished():
            QCoreApplication.processEvents()

        self.assertFalse(self.dialog.save_button.isEnabled())

    def test_connection_success(self):
        """Test for success test connection"""
        self.dialog.url_input.setText(self.url)
        self.dialog.username_input.setText(self.username)
        self.dialog.password_input.setText(self.password)
        button = self.dialog.test_connection_button
        button.click()

        while not self.dialog.login_api.reply.isFinished():
            QCoreApplication.processEvents()

        self.assertTrue(self.dialog.save_button.isEnabled())

        self.dialog.save_button.click()
        self.assertIsNotNone(get_authtoken())
        self.assertEqual(self.url, get_url_instance())


if __name__ == "__main__":
    suite = unittest.makeSuite(CadastaLoginDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
