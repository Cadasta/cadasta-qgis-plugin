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

__author__ = 'dimas@kartoza.com'
__revision__ = '$Format:%H$'
__date__ = '26/02/2014'
__copyright__ = 'Copyright 2016, Cadasta'


class Organization(object):
    """Organization api class"""

    api_url = 'https://demo.cadasta.org/api/v1/organizations/'

    def get_api(self, network):
        """
        Execute api get call
        :param network: NetworkMixin object
        :return: status request, if success returns json results, and if failed return failure messages
        """
        network.connect_get()
        while not network.reply.isFinished():
            QCoreApplication.processEvents()
        if not network.error:
            return True, network.get_json_results()
        else:
            return False, network.error

    def get_all_organizations(self):
        """
        Get all organizations
        :return: status request, list of organizations
        """
        network = NetworkMixin(self.api_url)
        return self.get_api(network)

    def get_summary_organization(self, slug):
        """
        Get detail summary organization
        :param slug: organization slug
        :return: status request, summary of organization
        """
        if not slug:
            return False, None
        network = NetworkMixin(self.api_url + slug + '/')
        return self.get_api(network)
