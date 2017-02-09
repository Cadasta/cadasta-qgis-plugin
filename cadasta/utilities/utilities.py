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
from cadasta.common.setting import get_path_data
from cadasta.utilities.resources import get_project_path

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class Utilities(object):
    """Class contains helpfull methods for cadasta process."""

    @staticmethod
    def save_project_basic_information(information):
        """Save project basic information.

        :param information: basic information that will be saved
        :type information: dict
        """
        organization_slug = information['organization']['slug']
        project_slug = information['slug']
        filename = get_path_data(
            organization_slug=organization_slug)

        filename = os.path.join(
            filename,
            '%s.json' % project_slug
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
    def get_basic_information_by_vector(layer):
        """Get basic information that already saved.

        :param layer: vector layer that will be checked
        :type layer: QgsVectorLayer

        :return: information
        :rtype: dict
        """
        # checking by names
        LOGGER.debug(layer.name())
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
