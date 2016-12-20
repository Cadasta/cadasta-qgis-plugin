# coding=utf-8

"""Tests for project api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

import os
from cadasta.api.project import Project
from qgis.PyQt.QtCore import QCoreApplication

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class ProjectTest(unittest.TestCase):
    """Test project api works."""

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_project(self):
        """Test we can click OK."""
        project = Project()
        # Wait until it finished
        while not project.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(project.get_json_results())


if __name__ == "__main__":
    suite = unittest.makeSuite(ProjectTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
