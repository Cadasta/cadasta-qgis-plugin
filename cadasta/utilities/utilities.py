# coding=utf-8
"""
Cadasta -**Cadasta Utilities.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import logging
import shapely.wkt
import geojson

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '27/12/2016'
__copyright__ = 'Copyright 2016, Cadasta'


LOGGER = logging.getLogger('CadastaQGISPlugin')


def convert_wkt_to_geojson(wkt):
    """Convert wkt string to geojson format string.

    :param wkt: Wkt format string
    :type wkt: str
    :returns: Geojson format string
    :rtype: str
    """
    wkt_geometry = shapely.wkt.loads(wkt)
    geojson_geometry = geojson.Feature(
        geometry=wkt_geometry,
        properties={}
    )

    geojson_string = geojson.dumps(
        geojson_geometry,
        sort_keys=True
    )

    return geojson_string
