# coding=utf-8
"""
Cadasta project - **Organization api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from qgis.PyQt.QtCore import QCoreApplication
from cadasta.mixin.network_mixin import NetworkMixin
from cadasta.common.setting import get_url_instance

__author__ = 'dimas@kartoza.com'
__revision__ = '$Format:%H$'
__date__ = '26/02/2014'
__copyright__ = 'Copyright 2016, Cadasta'


class Organization(object):
    """Class to fetch available organization data."""

    api_url = 'api/v1/organizations/'

    def _call_api(self, network):
        """Private method to execute api.

        :param network: NetworkMixin object
        :type network: NetworkMixin

        :return: Tuple status request and results,
                  if request failed returns failure messages.
        :rtype: (bool, list/dict/str)
        """
        network.connect_get()
        while not network.reply.isFinished():
            QCoreApplication.processEvents()
        if not network.error:
            return True, network.get_json_results()
        else:
            return False, network.error

    def all_organizations(self):
        """Get all organizations.

        :return: Tuple of status request and list of organizations
                  (if request failed return failure messages).
        :rtype: (bool, list/str)
        """
        network = NetworkMixin(get_url_instance() + self.api_url)
        return self._call_api(network)

    def organizations_project_filtered(self):
        """Get organizations with permission to list and add project.

        :return: Tuple of status request and list of organizations
                  (if request failed return failure messages).
        :rtype: (bool, list/str)
        """
        permissions = '?permissions=project.create,project.list'
        network = NetworkMixin(get_url_instance() + self.api_url + permissions)
        return self._call_api(network)

    def summary_organization(self, slug):
        """Get detail summary organization.

        :param slug: organization slug
        :type slug: str

        :return: Tuple of status request and summary of organization
                  (if request failed return failure messages).
        :rtype: (bool, dict/str)
        """
        if not slug:
            return False, None
        network = NetworkMixin(get_url_instance() + self.api_url + slug + '/')
        return self._call_api(network)
