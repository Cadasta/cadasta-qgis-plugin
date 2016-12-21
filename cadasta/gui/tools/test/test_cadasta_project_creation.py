# coding=utf-8
"""Cadasta project creation test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'dimas@kartoza.com'
__date__ = '2016-12-21'
__copyright__ = 'Copyright 2016, Kartoza'

import os
import unittest

from cadasta.gui.tools.cadasta_project_creation import CadastaProjectCreation

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class CadastaProjectCreationTest(unittest.TestCase):
    """Test project creation dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = CadastaProjectCreation()

    def test_get_available_organisations(self):
        """Test get available button works."""
        button = self.dialog.get_organisations_button
        button.click()
        self.assertIsInstance(self.dialog.organisations_list, list)

    def test_valid_form(self):
        """Check if form is valid."""
        url = 'google.com'
        self.dialog.project_url_input.setText(url)
        button = self.dialog.next_button
        button.click()
        self.assertTrue(self.dialog.form_valid_flag)
