# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'christian@kartoza.com'
__date__ = '2016-11-25'
__copyright__ = 'Copyright 2016, Kartoza'

import unittest
import os
import qgis
from cadasta.utilities.resources import (
    resources_path,
    resource_url,
    is_valid_url
)


class CadastaResourcesTest(unittest.TestCase):
    """Test rerources work."""

    def test_resources_url(self):
        """Test we can get the path as a local url nicely.

        .. versionadded:: 3.0
        """
        url = resource_url(
            resources_path(
                'img', 'logos', 'cadasta-logo.png'))
        self.assertTrue(
            'file://' in url,
            url + ' is not valid')

    def test_valid_url(self):
        """Test to check url validation."""
        url1 = 'google'
        url2 = 'http://www.kartoza.com'

        self.assertFalse(is_valid_url(url1))
        self.assertTrue(is_valid_url(url2))

if __name__ == '__main__':
    unittest.main()
