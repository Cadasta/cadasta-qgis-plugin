# coding=utf-8
"""
Cadasta Utilities -**Geojson Parser**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import copy
import json

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'


class GeojsonParser(object):
    """Class for parsing geojson."""
    original_geojson = None
    geojson = None

    def __init__(self, geojson):
        """Geojson that will be parsed.

        :param geojson: Json that will be parsed.
        :type geojson: dict/str
        """
        if isinstance(geojson, dict):
            self.original_geojson = geojson
        elif isinstance(geojson, basestring):
            self.original_geojson = json.loads(geojson)
        self.parse_geojson()

    def parse_geojson(self):
        """Parsing geojson, especially for not formatted geojson.
        """
        if self.original_geojson:
            self.geojson = copy.deepcopy(self.original_geojson)
            for feature in self.geojson['features']:
                new_properties = {}
                properties = feature['properties']
                for property_key, property_value in properties.iteritems():
                    if isinstance(property_value, dict):
                        for key, value in property_value.iteritems():
                            new_properties[key] = value
                    else:
                        new_properties[property_key] = property_value
                feature['properties'] = new_properties

    def get_geojson_for_qgis(self):
        """Parsing geojson, especially for not formatted geojson.
        """
        json = {}
        if self.original_geojson:
            geojson = copy.deepcopy(self.original_geojson)
            if len(geojson['features']) == 0:
                json['point'] = {
                    u'type': u'FeatureCollection', u'features': []
                }
            else:
                for feature in geojson['features']:
                    new_properties = {}
                    properties = feature['properties']
                    for property_key, property_value in properties.iteritems():
                        if isinstance(property_value, dict):
                            for key, value in property_value.iteritems():
                                new_properties[key] = value
                        else:
                            new_properties[property_key] = property_value
                    feature['properties'] = new_properties
                    # assign to json by type
                    type = feature['geometry']['type']
                    if type not in json:
                        json[type] = {
                            u'type': u'FeatureCollection', u'features': []
                        }
                    json[type]['features'].append(feature)
        return json

    def get_geojson(self):
        """Returning geojson in dict format.

        :return: geojson string
        :rtype: str
        """
        return self.geojson

    def geojson_string(self):
        """Returning geojson in string format.

        :return: geojson string
        :rtype: str
        """
        return json.dumps(self.geojson, sort_keys=True)

    def get_original_geojson(self):
        """Returning original geojson in dict format.

        :return: geojson string
        :rtype: str
        """
        return self.original_geojson

    def original_geojson_string(self):
        """Returning original geojson in string format.

        :return: geojson string
        :rtype: str
        """
        return json.dumps(self.original_geojson, sort_keys=True)
