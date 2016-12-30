# coding=utf-8
"""cadasta login test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import unittest

from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import QCoreApplication
from qgis.testing.mocked import get_iface
from qgis.utils import iface

from cadasta.common.setting import (
    get_authtoken,
    get_url_instance
)

from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.gui.tools.widget.options_widget import OptionsWidget

if iface:
    IFACE = iface
else:
    IFACE = get_iface()


class CadastaLoginTest(unittest.TestCase):
    """Test Login dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.url = 'https://demo.cadasta.org/'
        self.username = 'kartoza.demo'
        self.password = 'demo.kartoza1!'
        dialog = CadastaDialog(
            iface=IFACE,
            subtitle='Cadasta Login',
            widget=OptionsWidget()
        )
        self.dialog = dialog.widget

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
    suite = unittest.makeSuite(CadastaLoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
