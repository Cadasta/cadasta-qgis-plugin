# coding=utf-8

"""Tests for organization project api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

from mock.mock import MagicMock
from mock import patch
from qgis.testing.mocked import get_iface
from qgis.utils import iface
from cadasta.api.organization_project import (
    OrganizationProject,
    OrganizationProjectSpatial
)


if iface:
    QGIS_APP = iface
else:
    QGIS_APP = get_iface()


class OrganizationProjectTest(unittest.TestCase):
    """Test project api works."""

    test_projects = [
        {
            'id': "jmh29hm6h6ustekasu4d2qx7",
            'organization': {
                'id': "j9zk7y9hbrdfaeam5j7aampx",
                'slug': "any-given-sunday",
                'name': "Any Given Sunday",
                'description': "test",
                'archived': False,
                'urls': [
                    "https://dj-m.github.io"
                ],
                'contacts': []
            }
        }
    ]
    test_project_spatial = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -121.91062688827515,
                        37.25333811214945
                    ]
                },
                "properties": {
                    "id": "4cc3ciqyzyyxq6mxdegapy5a",
                    "type": "BU",
                    "attributes": {}
                }
            }
        ]
    }

    def setUp(self):
        """Runs before each test."""
        self.organization_slug = 'any-given-sunday'
        self.project_slug = 'san-jose-open-data'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    @patch("cadasta.api.organization_project."
           "OrganizationProject.__init__")
    def test_organization_project(self, mock_init):
        """Test organization project api."""
        mock_init.return_value = None
        organization_project = OrganizationProject(
            self.organization_slug)
        organization_project.get_json_results = MagicMock(
            return_value=(True, self.test_projects)
        )
        results = organization_project.get_json_results()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], list)

    @patch("cadasta.api.organization_project."
           "OrganizationProjectSpatial.__init__")
    def test_organization_project_spatial(self, mock_init):
        """Test organization project api spatial."""
        mock_init.return_value = None
        organization_project = OrganizationProjectSpatial(
            self.organization_slug, self.project_slug)
        organization_project.get_json_results = MagicMock(
            return_value=(True, self.test_project_spatial)
        )
        results = organization_project.get_json_results()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], dict)


if __name__ == "__main__":
    suite = unittest.makeSuite(OrganizationProjectTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
