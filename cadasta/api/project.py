# coding=utf-8
"""
Cadasta project - **Project api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from cadasta.api.base_api import BaseApi
from cadasta.common.setting import (
    get_url_instance,
    get_setting
)


__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'


class Project(BaseApi):
    """Class to fetch available project data."""

    api_url = 'api/v1/projects/'

    def __init__(self, on_finished=None):
        """Constructor.

        :param on_finished: (optional) function that catch result request
        :type on_finished: Function
        """
        self.request_url = get_url_instance() + self.api_url
        if not get_setting('public_project'):
            self.request_url += '?permissions=project.update'
        super(Project, self).__init__()
        self.on_finished = on_finished
        self.connect_get()

    def connection_finished(self):
        """On finished function when tools request is finished."""
        # extract result
        if self.error:
            self.on_finished(
                (False, self.error)
            )
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(
                    (True, result)
                )
