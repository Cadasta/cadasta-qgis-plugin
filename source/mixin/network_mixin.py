from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
import datetime


class NetworkMixin(QNetworkAccessManager):
    request_url = str
    result_connection = ""

    def __init__(self):
        QNetworkAccessManager.__init__(self)
        self.reply = QNetworkReply()
        self.result_connection += QByteArray()
        url = QUrl(self.request_url)
        self.req = QNetworkRequest(url)

    def connection_finished(self):
        print('finish')
        print(self.result_connection)

    @pyqtSlot()
    def connection_read_data(self):
        self.result_connection += self.reply.readAll()

    def connect_request(self):
        self.reply.readyRead.connect(self.connection_read_data)
        self.reply.finished.connect(self.connection_finished)

    def connect_get(self):
        self.reply = self.get(self.req)
        self.connect_request()

    def connect_post(self, data):
        self.reply = self.post(self.req, data)
        self.connect_request()
