# -*- coding: utf-8 -*-
import json
from source.mixin.network_mixin import NetworkMixin
from qgis.PyQt import pyqtSlot, QByteArray

URL_TARGET = 'https://platform-staging-api.cadasta.org/api/v1/'


class Login(NetworkMixin):
    # LOGIN class
    request_url = URL_TARGET + 'account/login/?'

    def __init__(self, USERNAME, PASSWORD, output_label):
        NetworkMixin.__init__(self)
        # extract data
        postData = QByteArray()
        postData.append("username=%s&" % USERNAME)
        postData.append("password=%s" % PASSWORD)
        self.output_label = output_label
        self.connectPOST(postData)

    @pyqtSlot()
    def connectionFinished(self):
        # extract result
        result = self.result_connection.data()
        result = json.loads(result)
        # check result
        if 'auth_token' in result:
            auth_token = result['auth_token']
            output_result = "auth_token is %s" % auth_token
        else:
            output_result = result
        self.label_3.setText(output_result)
