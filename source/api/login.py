# -*- coding: utf-8 -*-
import json
from source.mixin.network_mixin import NetworkMixin
from qgis.PyQt.QtCore import pyqtSlot, QByteArray

URL_TARGET = 'https://platform-staging-api.cadasta.org/api/v1/'


class Login(NetworkMixin):
    # LOGIN class
    request_url = URL_TARGET + 'account/login/?'

    def __init__(self, USERNAME, PASSWORD, output_label):
        NetworkMixin.__init__(self)
        # extract data
        post_data = QByteArray()
        post_data.append("username=%s&" % USERNAME)
        post_data.append("password=%s" % PASSWORD)
        self.output_label = output_label
        self.connect_post(post_data)

    @pyqtSlot()
    def connection_finished(self):
        # extract result
        result = self.result_connection.data()
        result = json.loads(result)
        # check result
        if 'auth_token' in result:
            auth_token = result['auth_token']
            output_result = "auth_token is %s" % auth_token
        else:
            output_result = result
        self.output_label.setText(output_result)
