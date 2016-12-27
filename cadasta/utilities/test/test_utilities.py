# coding=utf-8
"""Utilities test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'dimas@kartoza.com'
__date__ = '2016-11-25'
__copyright__ = 'Copyright 2016, Kartoza'

import unittest
import os
import qgis
import shapely.wkt
import geojson
from cadasta.utilities.utilities import (
    convert_wkt_to_geojson
)


class CadastaUtilitiesTest(unittest.TestCase):
    """Test utilities work."""

    def test_convert_wkt_to_geojson(self):
        """Test we can convert wkt to geojson string.
        """
        wkt_string = 'POLYGON((91.22841324832725718 6.83284828351750306, ' \
                     '104.92860319259187918 6.83284828351750306, ' \
                     '104.92860319259187918 12.37548220617433614, ' \
                     '91.22841324832725718 12.37548220617433614, ' \
                     '91.22841324832725718 6.83284828351750306))'
        geojson_string = convert_wkt_to_geojson(wkt_string)
        self.assertIsNotNone(geojson_string)

if __name__ == '__main__':
    unittest.main()
