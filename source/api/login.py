# -*- coding: utf-8 -*-
import json
from source.mixin.network_mixin import NetworkMixin
from qgis.PyQt.QtCore import QByteArray

URL_TARGET = 'https://platform-staging-api.cadasta.org/api/v1/'


class Login(NetworkMixin):
    request_url = URL_TARGET + 'account/login/?'

    def __init__(self, username, password, on_finished=None):
        super(Login, self).__init__(self.request_url)
        post_data = QByteArray()
        post_data.append("username=%s&" % username)
        post_data.append("password=%s" % password)

        self.connect_post(post_data)
        self.on_finished = on_finished

    def connection_finished(self):
        # extract result
        result = json.loads(str(self.reply.readAll()))
        if self.on_finished and callable(self.on_finished):
            self.on_finished(result)
