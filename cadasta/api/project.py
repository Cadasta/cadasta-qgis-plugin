# coding=utf-8
"""
Cadasta project - **Project api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from cadasta.mixin.network_mixin import NetworkMixin
from cadasta.common.setting import get_url_instance

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'


class Project(NetworkMixin):
    """Class to fetch available organization data."""

    api_url = 'api/v1/projects/'

    def __init__(self, on_finished=None):
        """Constructor.

        :param on_finished: (optional) function that catch result request
        :type on_finished: Function
        """
        self.request_url = get_url_instance() + self.api_url
        super(Project, self).__init__()
        self.connect_get()
        self.on_finished = on_finished

    def connection_finished(self):
        """On finished function when tools request is finished."""
        # extract result
        if self.error:
            self.on_finished(self.error)
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(result)
