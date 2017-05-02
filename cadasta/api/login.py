# -*- coding: utf-8 -*-
"""
Cadasta project - **Login api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
from cadasta.api.base_api import BaseApi
from PyQt4.QtCore import QByteArray

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '16/12/16'
__copyright__ = 'Copyright 2016, Cadasta'


class Login(BaseApi):

    post_data = QByteArray()

    def __init__(self, domain, username, password, on_finished=None):
        """Constructor.

        Constructor of login class needs domain, username and password
        for check connection.

        :param username: username for login.
        :type username: QString

        :param password: username for login.
        :type password: QString

        :param on_finished: (optional) is a function that
                            catch tools result request.
        :type on_finished: Function
        """
        self.request_url = domain + 'api/v1/account/login/?'
        super(Login, self).__init__()
        self.post_data.append("username=%s&" % username)
        self.post_data.append("password=%s" % password)

        self.on_finished = on_finished

    def connection_finished(self):
        """Function finished handler.

        When tools request is finished, this function will be called.
        Try get result from self.get_json_results() in json format"""
        # extract result
        if self.error:
            self.on_finished(self.error)
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(result)
