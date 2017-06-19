# coding=utf-8
"""
Cadasta project - **Api connector.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from PyQt4.QtCore import QCoreApplication
from cadasta.mixin.network_mixin import NetworkMixin

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '04/01/17'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ApiConnect(NetworkMixin):
    """Class to call cadasta API."""

    def get(self, paginated=False):
        """Call get method.

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        if paginated:
            self.connect_get_paginated()
        else:
            self.connect_get()

        while not self.is_finished(paginated):
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.get_json_results()
        else:
            return False, \
                   '{"code" : %s, "result": %s}' % (
                       str(self.http_code), self.results.data()
                   )

    def patch_json(self, post_data):
        """Call patch method with json data.
        Use this method to send PATCH request with
        json string data.

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_json_patch(post_data)
        while not self.is_finished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.get_json_results()
        else:
            return False, \
                   '{"code" : %s, "result": %s}' % (
                       str(self.http_code), self.results.data()
                   )

    def put_json(self, post_data):
        """Call put method with json data.
        Use this method to send PUT request with
        json string data.

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_json_put(post_data)
        while not self.is_finished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.results.data()
        else:
            return False, \
                   '{"code" : %s, "result": %s}' % (
                       str(self.http_code), self.results.data()
                   )

    def post(self, post_data):
        """Call post method.

        :param post_data: data to post
        :type post_data: QByteArray

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        self.connect_post(post_data)
        while not self.is_finished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.get_json_results()
        else:
            return False, \
                   '{"code" : %s, "result": %s}' % (
                       str(self.http_code), self.results.data()
                   )

    def post_json(self, post_data):
        """Call post method with json string.

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, dict )
        """
        self.connect_json_post(post_data)
        while not self.is_finished():
            QCoreApplication.processEvents()

        if not self.error:
            return True, self.get_json_results()
        else:
            return False, \
                   '{"code" : %s, "result": %s}' % (
                       str(self.http_code), self.results.data()
                   )
