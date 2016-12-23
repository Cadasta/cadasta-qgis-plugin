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

import os
import unittest
from qgis.PyQt.QtCore import QCoreApplication

from cadasta.gui.tools.cadasta_project_download_step_2 import (
    CadastaProjectDownloadStep2
)

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class CadastaProjectDownloadDialogTest(unittest.TestCase):
    """Test project download dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.url = 'https://demo.cadasta.org/'
        self.slug = 'any-given-sunday'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_get_projects(self):
        """Test get project connection"""
        self.dialog = CadastaProjectDownloadStep2(self.slug)

        while not self.dialog.api.reply.isFinished():
            QCoreApplication.processEvents()

        self.assertIsNotNone(self.dialog.projects)


if __name__ == "__main__":
    suite = unittest.makeSuite(CadastaProjectDownloadDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
