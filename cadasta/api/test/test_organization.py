# coding=utf-8
__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '19/12/16'

import unittest

import os
from cadasta.api.organization import Organization

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app
    QGIS_APP = get_qgis_app()


class LoginTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.username = 'kartoza.demo'
        self.password = 'demo.kartoza1!'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_get_all_organizations(self):
        """Test we get all organization."""
        organization = Organization()
        results = organization.get_all_organizations()
        self.assertTrue(results[0])
        self.assertIsNotNone(results[1])

    def test_get_summary_organization(self):
        """Test we get one organization by slug"""
        slug = 'allthethings'
        organization = Organization()
        results = organization.get_summary_organization(slug)
        self.assertTrue(results[0])
        self.assertIsNotNone(results[1])

    def test_error_get_all_organizations(self):
        """Test if it gives correct error messages"""
        organization = Organization()
        organization.api_url = 'https://demo.cadasta.org/api/v2/organizations/'
        results = organization.get_all_organizations()
        self.assertFalse(results[0])
        self.assertIn('404', results[1])


if __name__ == "__main__":
    suite = unittest.makeSuite(LoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
