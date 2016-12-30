# coding=utf-8
"""cadasta project download test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import os
import unittest

from mock.mock import MagicMock
from qgis.PyQt.QtCore import QCoreApplication
from qgis.testing.mocked import get_iface
from qgis.utils import iface
from cadasta.gui.tools.wizard.project_download_wizard import (
    ProjectDownloadWizard
)

if iface:
    IFACE = iface
else:
    IFACE = get_iface()


class CadastaProjectDownloadWizardTest(unittest.TestCase):
    """Test project download dialog works."""
    test_project = {
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
        self.url = 'https://demo.cadasta.org/'
        self.dialog = ProjectDownloadWizard(iface=IFACE)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_step_01(self):
        """Test step 01"""
        current_step = self.dialog.get_current_step()
        button = current_step.get_available_projects_button
        button.click()

        while not current_step.project_api.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(current_step.selected_project())

    def test_step_02(self):
        """Test step 02"""
        current_step = self.dialog.get_current_step()
        current_step.selected_project = MagicMock(
            return_value=self.test_project
        )
        self.dialog.next_button.click()
        current_step = self.dialog.get_current_step()
        while not current_step.spatial_api.reply.isFinished():
            QCoreApplication.processEvents()

        self.assertTrue(self.dialog.next_button.isEnabled())


if __name__ == "__main__":
    suite = unittest.makeSuite(CadastaProjectDownloadWizardTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
