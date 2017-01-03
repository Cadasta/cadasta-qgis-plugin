# coding=utf-8
"""Cadasta project update test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'dimas@kartoza.com'
__date__ = '2017-01-01'
__copyright__ = 'Copyright 2016, Kartoza'

import unittest
from mock import MagicMock
from qgis.testing.mocked import get_iface
from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface

from cadasta.gui.tools.wizard.project_update_wizard import (
    ProjectUpdateWizard
)

if iface:
    IFACE = iface
else:
    IFACE = get_iface()


class CadastaProjectCreationTest(unittest.TestCase):
    """Test project update dialog works."""

    test_project = {
        'name': 'test project',
        'description': '',
        'urls': [''],
        'access': 'private',
        'contacts': [],
        'id': "jmh29hm6h6ustekasu4d2qx7",
        'organization': {
            'id': "j9zk7y9hbrdfaeam5j7aampx",
            'slug': "any-given-sunday",
            'name': "Any Given Sunday",
            'description': "Mapping & drawing publicly "
                           "available municipal datasets "
                           "in the interest of sussing out "
                           "unforeseen relationships",
        },
        'slug': "san-jose-open-data-portal-affordable-housing"
    }

    def setUp(self):
        """Runs before each test."""
        self.wizard = ProjectUpdateWizard(iface=IFACE)

    def test_step_01(self):
        """Test step 01"""
        current_step = self.wizard.get_current_step()
        button = current_step.get_available_projects_button
        button.click()

        while not current_step.project_api.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(current_step.selected_project())

    def test_step_02(self):
        """Test step 02"""
        current_step = self.wizard.step_project_update02
        current_step.parent.project = self.test_project
        current_step.send_update_request = MagicMock(
                return_value=(True, '')
        )
        current_step.update_button.click()
        self.assertEqual(
                current_step.update_status_label.text(),
                'Update success'
        )
