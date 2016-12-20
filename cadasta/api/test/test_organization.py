# coding=utf-8

"""Tests for organization api.
"""

import unittest

import os
from mock.mock import MagicMock
from cadasta.api.organization import Organization

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '19/12/16'


if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app
    QGIS_APP = get_qgis_app()


class OrganizationTest(unittest.TestCase):
    """Test Organization api
    """

    test_organization = {
        'id': 'yzqz5vup4cvz3ukfsyvstdfb',
        'slug': 'allthethings',
        'name': 'AllTheThings',
        'description': '',
        'archived': 'false',
        'urls': [],
        'contacts': []
    }

    def test_get_all_organizations(self):
        """Test we get all organization."""
        organization = Organization()
        organization._call_api = MagicMock(
                return_value=(True, [self.test_organization])
        )
        results = organization.all_organizations()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], list)

    def test_get_summary_organization(self):
        """Test we get one organization by slug."""
        slug = 'allthethings'
        organization = Organization()
        organization._call_api = MagicMock(
                return_value=(True, self.test_organization)
        )
        results = organization.summary_organization(slug)
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], dict)

    def test_error_get_all_organizations(self):
        """Test if it gives correct error messages."""
        organization = Organization()
        organization._call_api = MagicMock(
                return_value=(False, '404')
        )
        results = organization.all_organizations()
        self.assertFalse(results[0])
        self.assertIn('404', results[1])


if __name__ == "__main__":
    suite = unittest.makeSuite(OrganizationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
