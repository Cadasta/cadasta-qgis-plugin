import logging
import abc
import json
from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtNetwork import (
    QNetworkReply,
    QNetworkRequest,
)
from qgis.PyQt.QtCore import QUrl, QByteArray
from cadasta.common.setting import get_authtoken

LOGGER = logging.getLogger('CadastaQGISPlugin')

__author__ = 'dimas.ciputra@gmail.com'
__date__ = '15/12/2016'


class NetworkMixin(object):
    """A mixin that can be used to send network request and receive replies."""

    request_url = str
    error = None
    results = None

    def __init__(self, request_url=None):
        if request_url is not None:
            self.request_url = request_url
        self.manager = QgsNetworkAccessManager.instance()
        self.reply = None
        self.url = QUrl(self.request_url)
        self.req = QNetworkRequest(self.url)
        self.results = QByteArray()
        self.auth_token = get_authtoken()

    def connect_request(self):
        """Process the request."""
        LOGGER.info('Requesting...')
        self.reply.readyRead.connect(self.connection_read_data)
        self.reply.finished.connect(self.connection_finished)
        self.reply.error.connect(self.connection_error)

    def connect_get(self):
        """Send get request."""
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader('Authorization', 'token %s' % self.auth_token)
        self.reply = self.manager.get(self.req)
        self.connect_request()

    def connect_post(self, data):
        """Send post request.

        :param data: Context data to use with template
        :type data: QByteArray
        """
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader('Authorization', 'token %s' % self.auth_token)
        self.reply = self.manager.post(self.req, data)
        self.connect_request()

    def connection_read_data(self):
        """Get data from self.reply and append it to results."""
        self.results += self.reply.readAll()

    def get_json_results(self):
        """Convert results to json object."""
        return json.loads(str(self.results))

    def connection_error(self):
        """Handle error connection."""
        error_result = self.reply.error

        try:
            http_code = int(self.reply.attribute(
                QNetworkRequest.HttpStatusCodeAttribute))
        except TypeError:
            http_code = None

        if error_result == QNetworkReply.UnknownNetworkError:
            msg = 'The network is unreachable.'
        elif error_result == QNetworkReply.ProtocolUnknownError\
                or error_result == QNetworkReply.HostNotFoundError:
            msg = 'Host not found : %s' % self.url.encodedHost()
        else:
            if http_code:
                msg = 'Error code:' + str(http_code)
            else:
                msg = 'Can\'t find the server'

        LOGGER.debug(msg)
        self.error = msg

    @abc.abstractmethod
    def connection_finished(self):
        return
