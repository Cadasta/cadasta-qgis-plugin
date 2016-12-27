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
from mock import MagicMock

from cadasta.gui.tools.wizard.project_creation_wizard import (
    ProjectCreationWizard
)

from cadasta.test.utilities import get_qgis_app
QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()


class CadastaProjectCreationTest(unittest.TestCase):
    """Test project creation dialog works."""

    test_organization = [{
        'id': 'yzqz5vup4cvz3ukfsyvstdfb',
        'slug': 'allthethings',
        'name': 'AllTheThings',
        'description': '',
        'archived': 'false',
        'urls': [],
        'contacts': []
    }]

    def setUp(self):
        """Runs before each test."""
        self.wizard = ProjectCreationWizard(iface=IFACE)
        self.step1 = self.wizard.step_project_creation01
        self.step1.organisation._call_api = MagicMock(
                return_value=(True, self.test_organization)
        )
        self.step2 = self.wizard.step_project_creation02
        self.step3 = self.wizard.step_project_creation03

    def test_get_available_organisations(self):
        """Test get available button works in step 1."""
        button = self.step1.get_organisation_button
        button.click()
        self.assertIsInstance(self.wizard.organisations_list, list)

    def test_valid_form(self):
        """Check if form is valid."""
        url = 'http://www.google.com'
        project_name = 'project_name'
        button = self.step1.get_organisation_button
        button.click()
        self.step1.project_url_text.setText(url)
        self.step1.project_name_text.setText(project_name)
        self.assertTrue(self.step1.validate_step())
