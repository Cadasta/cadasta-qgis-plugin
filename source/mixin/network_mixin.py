from PyQt4.QtCore import *
from PyQt4.QtNetwork import *


class NetworkMixin(QNetworkAccessManager):
    request_url = str
    result_connection = ""

    @pyqtSlot()
    def connectionFinished(self):
        print(self.result_connection)

    @pyqtSlot()
    def connectionReadData(self):
        self.result_connection += self.reply.readAll()

    def connect(self):
        QObject.connect(
            self.reply, SIGNAL('readyRead()'),
            self, SLOT('connectionReadData()'))

        QObject.connect(
            self.reply, SIGNAL('finished()'),
            self, SLOT('connectionFinished()'))

    def connectGET(self):
        self.reply = self.get(self.req)
        self.connect()

    def connectPOST(self, data):
        self.reply = self.post(self.req, data)
        self.connect()

    def __init__(self):
        QNetworkAccessManager.__init__(self)
        self.result_connection += QByteArray()
        url = QUrl(self.request_url)
        self.req = QNetworkRequest(url)
