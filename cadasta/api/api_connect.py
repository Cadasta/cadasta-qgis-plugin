# coding=utf-8
"""
Cadasta project - **Api connector.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from qgis.PyQt.QtCore import QCoreApplication
from cadasta.mixin.network_mixin import NetworkMixin

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '04/01/17'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ApiConnect(NetworkMixin):
    """Class to call cadasta API."""

    def __init__(self, api_url):
        """Constructor.

        :param api_url: url for connection
        :type api_url: str
        """
        self.request_url = api_url
        super(ApiConnect, self).__init__()

    def get(self):
        """Call get method.

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_get()
        while not self.reply.isFinished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.get_json_results()
        else:
            return False, self.results.data()

    def patch_json(self, post_data):
        """Call patch method with json data.

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_json_patch(post_data)
        while not self.reply.isFinished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.results.data()
        else:
            return False, self.results.data()

    def post(self, post_data):
        """Call post method.

        :param post_data: data to post
        :type post_data: QByteArray

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_post(post_data)
        while not self.reply.isFinished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.results.data()
        else:
            return False, self.results.data()

    def post_json(self, post_data):
        """Call post method with json string.

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_json_post(post_data)
        while not self.reply.isFinished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.results.data()
        else:
            return False, self.results.data()
