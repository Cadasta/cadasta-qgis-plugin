# -*- coding: utf-8 -*-
import json
from cadasta.mixin.network_mixin import NetworkMixin
from qgis.PyQt.QtCore import QByteArray


class Login(NetworkMixin):
    def __init__(self, domain, username, password, on_finished=None):
        """
        Constructor
        :param username:
        :param password:
        :param on_finished: is a function that catch tools result request
        :return:
        """
        self.request_url = domain + 'api/v1/account/login/?'
        super(Login, self).__init__()
        post_data = QByteArray()
        post_data.append("username=%s&" % username)
        post_data.append("password=%s" % password)

        self.connect_post(post_data)
        self.on_finished = on_finished

    def connection_finished(self):
        """On finished function when tools request is finished"""
        # extract result
        if self.error:
            self.on_finished(self.error)
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(result)
