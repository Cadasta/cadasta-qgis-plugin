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
from PyQt4.QtCore import QCoreApplication
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
        self.wizard = ProjectUpdateWizard(iface=IFACE)
        self.step1 = self.wizard.step_project_update01
        self.step1.organization._call_api = MagicMock(
            return_value=(True, self.test_organization)
        )
        self.step1.get_downloaded_project = MagicMock(
            return_value=[self.test_project]
        )

    def test_step_01(self):
        """Test step 01"""
        current_step = self.wizard.get_current_step()
        button = current_step.get_available_projects_button
        button.click()
        self.assertIsNotNone(current_step.selected_project())
