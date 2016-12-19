# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'christian@kartoza.com'
__date__ = '2016-11-25'
__copyright__ = 'Copyright 2016, Kartoza'

import unittest

from qgis.gui import QgsMessageBar

from cadasta.gui.tools.cadasta_login import CadastaLogin


class CadastaLoginTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = CadastaLogin(None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_warning_message(self):
        """Test warning message bar shows up if username/password is empty"""
        button = self.dialog.test_connection_button
        button.click()
        msg_bar = self.dialog.msg_bar
        self.assertIsInstance(msg_bar, QgsMessageBar)

if __name__ == "__main__":
    suite = unittest.makeSuite(CadastaLoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
