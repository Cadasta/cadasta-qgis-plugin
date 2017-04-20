# coding=utf-8
"""
Cadasta project - **Base Api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from cadasta.mixin.network_mixin import NetworkMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '18/01/17'
__copyright__ = 'Copyright 2016, Cadasta'


class BaseApi(NetworkMixin):
    """Base API using NetworkMixin."""

    def __init__(self, request_url, on_finished=None, *args, **kwargs):
        """Constructor.

        :param on_finished: (optional) function that catch result request
        :type on_finished: Function
        """
        self.on_finished = on_finished
        super(BaseApi, self).__init__(request_url, *args, **kwargs)

    def connection_finished(self):
        """On finished function when tools request is finished."""
        # extract result
        if self.error:
            self.on_finished((False, self.error))
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished((True, result))
