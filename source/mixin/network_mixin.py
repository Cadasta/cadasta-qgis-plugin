import abc
from qgis.PyQt.QtNetwork import *
from qgis.PyQt.QtCore import *


class NetworkMixin(object):
    def __init__(self, request_url):
        self.manager = QNetworkAccessManager()
        self.reply = QNetworkReply
        self.req = QNetworkRequest(QUrl(request_url))

    def connect_request(self):
        self.reply.readyRead.connect(self.connection_read_data)
        self.reply.finished.connect(self.connection_finished)

    def connect_get(self):
        # GET connection
        self.reply = self.manager.get(self.req)
        self.connect_request()

    def connect_post(self, data):
        # POST connection
        self.reply = self.manager.post(self.req, data)
        self.connect_request()

    @abc.abstractmethod
    def connection_read_data(self):
        return

    @abc.abstractmethod
    def connection_finished(self):
        return
