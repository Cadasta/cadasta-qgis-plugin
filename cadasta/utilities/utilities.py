# coding=utf-8
"""
Cadasta Utilities -**Utilities**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import csv
import json
import logging
import os
import shutil
from qgis.core import (
    QgsVectorLayer,
    QgsMapLayerRegistry,
    QgsVectorFileWriter,
    QgsFeature,
    QGis)
from cadasta.common.setting import get_path_data, get_csv_path
from cadasta.utilities.geojson_parser import GeojsonParser
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import get_project_path
from cadasta.model.contact import Contact

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class Utilities(object):
    """Class contains helpful methods for cadasta process."""

    @staticmethod
    def delete_geojson_and_information(layers):
        """Save project basic information.

        :param layers: vector layer that will be checked
        :type layers: [QgsVectorLayer]
        """
        for layer in layers:
            qgis_layer = QgsMapLayerRegistry.instance().mapLayer(layer)
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
                if fname.endswith('.geojson'):
                    geojson_present = True
                    break
            if not geojson_present:
                try:
                    shutil.rmtree(project_folder)
                except OSError:
                    pass

    @staticmethod
    def save_project_basic_information(
            information,
            vlayers=None,
            relationship_layer_id=None,
            party_layer_id=None):
        """Save project basic information.

        :param information: basic information that will be saved
        :type information: dict

        :param vlayers: list of Spatial vector layers
        :type vlayers: list of QgsVectorLayer

        :param relationship_layer_id: Id for relationship layer
        :type relationship_layer_id: str

        :param party_layer_id: Id for party layer
        :type party_layer_id: str
        """
        organization_slug = information['organization']['slug']
        project_slug = information['slug']

        # Save new contacts to db
        if 'contacts' in information:
            project_contacts = information['contacts']

            for contact in project_contacts:

                contact_from_db = Contact.get_rows(
                    name=contact['name'],
                    phone=contact['tel'],
                    email=contact['email']
                )

                if not contact_from_db:
                    new_contact = Contact()
                    new_contact.name = contact['name']
                    new_contact.email = contact['email']
                    new_contact.phone = contact['tel']
                    new_contact.save()

        filename = get_path_data(
            organization_slug=organization_slug,
            project_slug=project_slug)

        filename = os.path.join(
            filename,
            'information.json'
        )

        if relationship_layer_id:
            information['relationship_layer_id'] = relationship_layer_id

        if party_layer_id:
            information['party_layer_id'] = party_layer_id

        if vlayers:
            information['layers'] = []
            for layer in vlayers:
                layer_type = ''
                if layer.geometryType() == QGis.Point:
                    layer_type = 'Point'
                elif layer.geometryType() == QGis.Polygon:
                    layer_type = 'Polygon'
                elif layer.geometryType() == QGis.Line:
                    layer_type = 'Line'
                information['layers'].append(
                    {
                        'id': layer.id(),
                        'type': layer_type
                    }
                )

        file_ = open(filename, 'w')
        file_.write(json.dumps(information, sort_keys=True))
        file_.close()

    @staticmethod
    def update_project_basic_information(
            information,
            vlayers=None,
            relationship_layer_id=None,
            party_layer_id=None):
        """Update project basic information.

        :param information: basic information that will be saved
        :type information: dict

        :param vlayers: list of Spatial vector layers
        :type vlayers: list of QgsVectorLayer

        :param relationship_layer_id: Id for relationship layer
        :type relationship_layer_id: str

        :param party_layer_id: Id for party layer
        :type party_layer_id: str
        """
        organization_slug = information['organization']['slug']
        project_slug = information['slug']
        old_information = Utilities.get_basic_information(
            organization_slug,
            project_slug)

        information['relationship_layer_id'] = \
            old_information['relationship_layer_id']
        information['party_layer_id'] = \
            old_information['party_layer_id']

        Utilities.save_project_basic_information(
            information,
            vlayers,
            relationship_layer_id,
            party_layer_id
        )

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
                if Utilities.is_windows():
                    splitter = '\\'
                else:
                    splitter = '/'
                source = source[0].split(splitter)
                if len(source) >= 3:
                    # -1 is type layer
                    type = source[-1]
                    project_slug = source[-2]
                    organization_slug = source[-3]
                    return organization_slug, project_slug, type

        names = layer.name().split('/')
        if len(names) == 3:
            try:
                organization_slug = names[0]
                project_slug = names[1]
                type = names[3]
                return organization_slug, project_slug, type
            except IndexError:
                pass

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

        :return: layers
        :rtype: [QgsVectorLayer]
        """
        geojson = GeojsonParser(geojson)
        filename = get_path_data(
            organization_slug=organization_slug,
            project_slug=project_slug)

        if not os.path.exists(filename):
            os.makedirs(filename)

        layers = geojson.get_geojson_for_qgis()
        vlayers = []
        for key, value in layers.iteritems():
            geojson_name = os.path.join(
                filename,
                '%s.geojson' % key
            )
            file_ = open(geojson_name, 'w')
            file_.write(json.dumps(value, sort_keys=True))
            file_.close()
            vlayer = QgsVectorLayer(
                geojson_name, "%s/%s/%s" % (
                    organization_slug, project_slug, key
                ),
                "ogr"
            )
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)
            vlayers.append(vlayer)
        return vlayers

    @staticmethod
    def get_downloaded_projects(organization):
        """Get all downloaded projects.

        :return: downloaded projects
        :rtype: list of dict
        """
        file_path = get_path_data(organization)

        list_files = []

        for dirpath, _, filenames in os.walk(file_path):
            for f in filenames:
                if 'geojson' in f:
                    if Utilities.is_windows():
                        splitter = '\\'
                    else:
                        splitter = '/'
                    abs_path = os.path.abspath(
                            os.path.join(dirpath, f)).split('.')[1].split(
                            splitter)
                    names = []
                    names.append(abs_path[-3])
                    names.append(abs_path[-2])
                    names.append(abs_path[-1])
                    list_files.append(
                        '/'.join(names)
                    )

        projects = []

        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.name() in list_files:
                information = \
                    Utilities.get_basic_information_by_vector(layer)

                projects.append({
                    'id': layer.id(),
                    'name': layer.name(),
                    'information': information,
                    'vector_layer': layer
                })

        return projects

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
                reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                next(reader, None)
                layer.startEditing()
                for row in reader:
                    feature = QgsFeature()
                    feature.setAttributes(row)
                    layer.addFeature(feature, True)
                layer.commitChanges()

    @staticmethod
    def is_windows():
        """Check if qgis running on windows

        :return: boolean
        """
        return os.name == 'nt'

    @staticmethod
    def extract_error_detail(result):
        """Extract detail of error of connection

        :param result: result of connection
        :type result: str

        :return: detail result
        :rtype:str
        """
        error_detail = tr('Error : ')
        detail = ''
        try:
            json_result = json.loads(result)
            detail = json_result['result']['detail']
            code = json_result['code']
            error_detail = tr('Error %s : ' % str(code))
        except (TypeError, ValueError, KeyError):
            detail = result
        error_detail += detail
        return '<span style="color:red">%s</span><br>' % error_detail
