# coding=utf-8
"""
Cadasta Utilities -**Utilities**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import json
import logging
import os
import shutil
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from cadasta.common.setting import get_path_data
from cadasta.utilities.geojson_parser import GeojsonParser
from cadasta.utilities.resources import get_project_path

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class Utilities(object):
    """Class contains helpfull methods for cadasta process."""

    @staticmethod
    def delete_geojson_and_information(layers):
        """Save project basic information.

        :param layers: vector layer that will be checked
        :type layers: [QgsVectorLayer]
        """
        for layer in layers:
            LOGGER.debug(layer)
            qgis_layer = QgsMapLayerRegistry.instance().mapLayer(layer)
            LOGGER.debug(qgis_layer)
            organization_slug, project_slug, type = \
                Utilities.get_organization_project_slug(qgis_layer)
            project_folder = get_path_data(
                organization_slug=organization_slug,
                project_slug=project_slug)
            project_path = os.path.join(
                project_folder,
                '%s.geojson' % type
            )
            os.remove(project_path)

            # check geojson is not present
            geojson_present = False
            for fname in os.listdir(project_folder):
                LOGGER.debug(fname)
                if fname.endswith('.geojson'):
                    geojson_present = True
                    break
            if not geojson_present:
                try:
                    shutil.rmtree(project_folder)
                except OSError:
                    pass

    @staticmethod
    def save_project_basic_information(information):
        """Save project basic information.

        :param information: basic information that will be saved
        :type information: dict
        """
        organization_slug = information['organization']['slug']
        project_slug = information['slug']
        filename = get_path_data(
            organization_slug=organization_slug,
            project_slug=project_slug)

        filename = os.path.join(
            filename,
            'information.json'
        )
        file_ = open(filename, 'w')
        file_.write(json.dumps(information, sort_keys=True))
        file_.close()

    @staticmethod
    def get_basic_information(organization_slug, project_slug):
        """Get basic information that already saved.

        :param organization_slug: organization slug for data
        :type organization_slug: str

        :param project_slug: project_slug for data
        :type project_slug: str

        :return: information
        :rtype: dict
        """
        filename = get_path_data(
            organization_slug=organization_slug,
            project_slug=project_slug)
        filename = os.path.join(
            filename,
            'information.json'
        )
        if not os.path.isfile(filename):
            return {}

        try:
            file_ = open(filename, 'r')
            information = file_.read()
            file_.close()
            return json.loads(information)
        except TypeError:
            return {}

    @staticmethod
    def get_organization_project_slug(layer):
        """Get organization and project slug.

        :param layer: vector layer that will be checked
        :type layer: QgsVectorLayer

        :return: organization and project slug
        :rtype: tuple
        """

        data_path = get_project_path()
        data_path = os.path.join(
            data_path,
            'data'
        )
        # checking by source
        metadatas = layer.metadata().split('<p')
        for metadata in metadatas:
            if data_path in metadata:
                source = metadata.split('.geojson')
                source = source[0].split('/')
                if len(source) >= 3:
                    # -1 is type layer
                    type = source[-1]
                    project_slug = source[-2]
                    organization_slug = source[-3]
                    return organization_slug, project_slug, type

        names = layer.name().split('/')
        if len(names) == 3:
            organization_slug = names[0]
            project_slug = names[1]
            type = names[3]
            return organization_slug, project_slug, type

        return None, None, None

    @staticmethod
    def get_basic_information_by_vector(layer):
        """Get basic information that already saved.

        :param layer: vector layer that will be checked
        :type layer: QgsVectorLayer

        :return: information
        :rtype: dict
        """
        organization_slug, project_slug, type = \
            Utilities.get_organization_project_slug(layer)
        information = Utilities.get_basic_information(
            organization_slug, project_slug)
        information['layer_type'] = type
        return information

    @staticmethod
    def save_layer(geojson, organization_slug, project_slug):
        """Save geojson to local file.

        :param organization_slug: organization slug for data
        :type organization_slug: str

        :param project_slug: project_slug for getting spatial
        :type project_slug: str

        :param geojson: geojson that will be saved
        :type geojson: JSON object
        """
        geojson = GeojsonParser(geojson)
        filename = get_path_data(
            organization_slug=organization_slug,
            project_slug=project_slug)

        if not os.path.exists(filename):
            os.makedirs(filename)

        layers = geojson.get_geojson_for_qgis()
        for key, value in layers.iteritems():
            geojson_name = os.path.join(
                filename,
                '%s.geojson' % key
            )
            file_ = open(geojson_name, 'w')
            file_.write(json.dumps(value, sort_keys=True))
            file_.close()
            vlayer = QgsVectorLayer(
                geojson_name, "%s/%s/%s" % (organization_slug, project_slug, key), "ogr")
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)
