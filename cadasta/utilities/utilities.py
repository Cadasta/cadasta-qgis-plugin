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
import csv
from qgis.core import (
    QgsVectorLayer,
    QgsMapLayerRegistry,
    QgsVectorFileWriter,
    QgsFeature)
from cadasta.common.setting import get_path_data, get_csv_path
from cadasta.utilities.resources import get_project_path

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class Utilities(object):
    """Class contains helpful methods for cadasta process."""

    @staticmethod
    def save_project_basic_information(
            information,
            relationship_layer_id=None,
            party_layer_id=None):
        """Save project basic information.

        :param information: basic information that will be saved
        :type information: dict

        :param relationship_layer_id: Id for relationship layer
        :type relationship_layer_id: str

        :param party_layer_id: Id for party layer
        :type party_layer_id: str
        """
        organization_slug = information['organization']['slug']
        project_slug = information['slug']
        filename = get_path_data(
            organization_slug=organization_slug)

        filename = os.path.join(
            filename,
            '%s.json' % project_slug
        )

        if relationship_layer_id:
            information['relationship_layer_id'] = relationship_layer_id

        if party_layer_id:
            information['party_layer_id'] = party_layer_id

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
        filename = get_path_data(organization_slug)
        filename = os.path.join(
            filename,
            '%s.json' % project_slug
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
    def get_downloaded_projects(organization):
        """Get all downloaded projects.

        :return: downloaded projects
        :rtype: list of dict
        """
        file_path = get_path_data(organization)

        list_files = []

        for filename in os.listdir(file_path):
            if not os.path.isfile(os.path.join(file_path, filename)):
                continue
            if '.json' not in filename:
                continue
            project_name, file_extension = os.path.splitext(filename)
            list_files.append(organization + '/' + project_name)

        projects = []

        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.name() in list_files:
                project_slug = layer.name().split('/')[1]
                information = Utilities.get_basic_information(
                        organization,
                        project_slug)

                projects.append({
                    'id': layer.id(),
                    'name': layer.name(),
                    'information': information,
                    'vector_layer': layer
                })

        return projects

    @staticmethod
    def get_basic_information_by_vector(layer):
        """Get basic information that already saved.

        :param layer: vector layer that will be checked
        :type layer: QgsVectorLayer

        :return: information
        :rtype: dict
        """
        # checking by names
        names = layer.name().split('/')
        if len(names) == 2:
            organization_slug = names[0]
            project_slug = names[1]
            information = Utilities.get_basic_information(
                organization_slug, project_slug)
            if information:
                return information

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
                project_slug = names[-1]
                organization_slug = source[-2]
                information = Utilities.get_basic_information(
                    organization_slug, project_slug)
                return information

    @staticmethod
    def add_tabular_layer(
            tabular_layer,
            organization_slug,
            project_slug,
            attribute):
        """Add a tabular layer to the folder.

        :param tabular_layer: The layer to add.
        :type tabular_layer: QgsVectorLayer

        :param organization_slug: organization slug for data
        :type organization_slug: str

        :param project_slug: project_slug for getting spatial
        :type project_slug: str

        :param attribute: additional csv name
        :type attribute: str

        :returns: A two-tuple. The first element will be True if we could add
            the layer to the datastore. The second element will be the layer
            name which has been used or the error message.
        :rtype: (bool, str)
        """
        file_path = get_csv_path(organization_slug, project_slug, attribute)

        QgsVectorFileWriter.writeAsVectorFormat(
            tabular_layer,
            file_path,
            'utf-8',
            None,
            'CSV')

        return True, file_path

    @staticmethod
    def load_csv_file_to_layer(
            layer,
            organization_slug,
            project_slug,
            attribute):
        """Check if csv file is exist for layer,
        then add attribute from csv file to layer

        :param layer: layer to be added
        :type layer: QgsVectorLayer

        :param organization_slug: organization slug name
        :type organization_slug: str

        :param project_slug: project slug name
        :type project_slug: str

        :param attribute: additional csv attribute name
        :type attribute: str

        :return:
        """
        file_path = get_csv_path(organization_slug, project_slug, attribute)

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as csv_file:
                reader = csv.reader(csv_file, delimiter=',', quotechar='|')
                next(reader, None)
                layer.startEditing()
                for row in reader:
                    feature = QgsFeature()
                    feature.setAttributes(row)
                    layer.addFeature(feature, True)
                layer.commitChanges()
