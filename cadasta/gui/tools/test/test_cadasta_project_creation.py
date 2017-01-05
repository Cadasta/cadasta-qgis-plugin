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

import unittest
from mock import MagicMock
from qgis.testing.mocked import get_iface
from qgis.utils import iface

from cadasta.gui.tools.wizard.project_creation_wizard import (
    ProjectCreationWizard
)

if iface:
    IFACE = iface
else:
    IFACE = get_iface()


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

    def test_uploading_parties(self):
        """Test upload party"""
        self.step3.data = {
            "locations": {
                "features": [
                    {
                        "fields": {
                            "party_type": "IN",
                            "party_name": "TEST1"
                        },
                    },
                    {
                        "fields": {
                            "party_type": "GR",
                            "party_name": "TEST2"
                        },
                    }
                ]
            }
        }
        self.step3._url_post_parties = MagicMock(
            return_value='api-url'
        )
        self.step3._call_post = MagicMock(
            return_value=(True, '')
        )
        self.step3.upload_parties()
        self.assertEqual(
                self.step3.lbl_status.text(),
                'Finished uploading 2 party'
        )
        self.assertEqual(self.step3.progress_bar.value(), 100)

    def test_uploading_relationships(self):
        """Test upload relationship function."""
        self.step3.data = {
            "locations": {
                "features": [
                    {
                        "fields": {
                            "party_type": "IN",
                            "party_name": "TEST1",
                            "relationship_type": "LL"
                        },
                        "spatial_id": '1',
                        "party_id": '1',
                    },
                    {
                        "fields": {
                            "party_type": "GR",
                            "party_name": "TEST2",
                            "relationship_type": "LL"
                        },
                        "spatial_id": '2',
                        "party_id": '2',
                    }
                ]
            }
        }
        self.step3._url_post_relationships = MagicMock(
            return_value='api-url'
        )
        self.step3._call_post = MagicMock(
            return_value=(True, '')
        )
        self.step3.upload_relationships()
        self.assertEqual(
                self.step3.lbl_status.text(),
                'Finished uploading 2 relationship'
        )
        self.assertEqual(self.step3.progress_bar.value(), 100)
