# coding=utf-8

"""Tests for project api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

from mock.mock import MagicMock
from mock import patch
from cadasta.api.project import Project


class ProjectTest(unittest.TestCase):
    """Test project api works."""

    test_projects = [
        {
            'id': "jmh29hm6h6ustekasu4d2qx7",
            'organization': {
                'id': "j9zk7y9hbrdfaeam5j7aampx",
                'slug': "any-given-sunday",
                'name': "Any Given Sunday",
                'description': "",
                'archived': False,
                'urls': [
                    "https://dj-m.github.io"
                ],
                'contacts': []
            }
        }
    ]

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    @patch("cadasta.api.project.Project.__init__")
    def test_project(self, mock_init):
        """Test project api."""
        mock_init.return_value = None
        organization_project = Project()
        organization_project.get_json_results = MagicMock(
            return_value=(True, self.test_projects)
        )
        results = organization_project.get_json_results()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], list)


if __name__ == "__main__":
    suite = unittest.makeSuite(ProjectTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
