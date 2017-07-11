import functools
import logging
import abc
import json
from qgis.core import QgsNetworkAccessManager
from PyQt4.QtNetwork import (
    QNetworkReply,
    QNetworkRequest,
)
from PyQt4.QtCore import QUrl, QByteArray, QBuffer
from cadasta.common.setting import get_authtoken

LOGGER = logging.getLogger('CadastaQGISPlugin')

__author__ = 'dimas.ciputra@gmail.com'
__date__ = '15/12/2016'


class NetworkMixin(object):
    """A mixin that can be used to send network request and receive replies."""

    request_url = str
    error = None
    results = None

    def __init__(self, request_url, geojson=False):
        self.request_url = request_url
        self.manager = QgsNetworkAccessManager.instance()
        self.reply = None
        self.url = QUrl(self.request_url)
        self.req = QNetworkRequest(self.url)
        self.results = QByteArray()
        self.auth_token = get_authtoken()

        # Paginated data
        self._pagination_exhausted = False
        self.geojson = geojson
        if geojson:
            self.combine_new_data = self.combine_new_geojson_data

    def cancel_request(self):
        """Abort the request."""
        self.reply.abort()

    def connect_request(self):
        """Process the request."""
        LOGGER.info('Requesting "%s"', self.request_url)
        self.reply.readyRead.connect(self.connection_read_data)
        self.reply.finished.connect(self.connection_finished)
        self.reply.error.connect(self.connection_error)

    def connect_paginated_request(self, prev_data, callback):
        """Process the request of a paginated resource."""
        LOGGER.info('Requesting "%s" (paginated)', self.request_url)
        self.reply.readyRead.connect(self.connection_read_data)
        self.reply.finished.connect(functools.partial(
            self._handle_paginated_data, prev_data, callback))
        self.reply.error.connect(self.connection_error)

    def connect_get(self):
        """Send get request."""
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )
        self.reply = self.manager.get(self.req)
        self.connect_request()

    def connect_post(self, data):
        """Send post request.

        :param data: Context data to use with template
        :type data: QByteArray
        """
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )
        self.reply = self.manager.post(self.req, data)
        self.connect_request()

    def connect_json_post(self, data):
        """Send post request with json string.

        :param data: Json string data
        :type data: str
        """
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )
        self.req.setRawHeader("Content-Type", "application/json")
        self.reply = self.manager.post(self.req, data)
        self.connect_request()

    def connect_json_put(self, data):
        """Send put request with json string.

        :param data: Json string data
        :type data: str
        """
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )

        self.req.setRawHeader("Content-Type", "application/json")
        json_string = QByteArray(data)
        p_buffer = QBuffer(self.manager)
        p_buffer.setData(json_string)

        self.reply = self.manager.sendCustomRequest(
            self.req, 'PUT', p_buffer
        )
        self.connect_request()

    def connect_json_patch(self, data):
        """Send patch request with json string.

        :param data: Json string data
        :type data: str
        """
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )

        self.req.setRawHeader("Content-Type", "application/json")
        json_string = QByteArray(data)
        p_buffer = QBuffer(self.manager)
        p_buffer.setData(json_string)

        self.reply = self.manager.sendCustomRequest(
            self.req, 'PATCH', p_buffer
        )
        self.connect_request()

    def connect_get_paginated(self, prev_data=None, callback=None):
        if self.auth_token:
            # Add authentication token to request
            self.req.setRawHeader(
                'Authorization',
                'token %s' % self.auth_token
            )
        self.reply = self.manager.get(self.req)
        self.connect_paginated_request(
            prev_data or self.results,
            callback or self._set_results_and_complete
        )

    def _handle_paginated_data(self, prev_data, callback):
        """
        Once all data from single request is returned, merge it with
        previous responses and follow pagination.
        """
        # Add new request's data to prev_data
        resp_txt = str(self.results)
        merged_data = self.combine_new_data(str(prev_data or ''), resp_txt)
        merged_data = QByteArray(merged_data)

        # Get next page
        next_url = None
        try:
            next_url = json.loads(resp_txt).get('next')
        except ValueError:
            pass

        if next_url:
            next_req = NetworkMixin(next_url, geojson=self.geojson)
            return next_req.connect_get_paginated(
                prev_data=merged_data,
                callback=callback
            )

        LOGGER.debug('Pagination finished at "%s"', self.request_url)
        callback(merged_data)

    def _set_results_and_complete(self, results):
        self.results = results
        self._pagination_exhausted = True
        self.connection_finished()

    @staticmethod
    def combine_new_data(old_data_str, new_data_str):
        """
        Merge results from new page of data with results from previous
        pages of data.

        Expects a response in a format such as:
            {
                "count": 10,
                "next": null,
                "previous": null,
                "results": [ ... ]
            }
        """
        old_data = ''
        new_data = ''

        try:
            old_data = json.loads(old_data_str or '[]')
            new_data = json.loads(new_data_str)
        except ValueError:
            pass
        results_new_data = []
        if 'results' in new_data:
            results_new_data = new_data['results']
        return json.dumps(old_data + results_new_data)

    @staticmethod
    def combine_new_geojson_data(old_data_str, new_data_str):
        """
        Merge results from new page of GeoJSON data with results from
        previous pages of data.

        Expects a response in a format such as:
            {
                "count": 10,
                "next": null,
                "previous": null,
                "results": {
                    "type": "FeatureCollection",
                    "features": [ ... ]
                }
            }
        """
        old_data = dict()
        new_data = dict()
        try:
            old_data = json.loads(old_data_str or '[]')
            new_data = json.loads(new_data_str)
        except ValueError:
            pass

        if not old_data and 'results' in new_data:
            return json.dumps(new_data['results'])

        if 'features' in old_data and 'results' in new_data:
            old_data['features'] += new_data['results']['features']

        return json.dumps(old_data)

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

        self.http_code = 404
        if error_result == QNetworkReply.UnknownNetworkError:
            msg = 'The network is unreachable.'
        elif error_result == QNetworkReply.ProtocolUnknownError \
                or error_result == QNetworkReply.HostNotFoundError:
            msg = 'Host not found : %s' % self.url.encodedHost()
        else:
            if http_code:
                msg = 'Error code:' + str(http_code)
                self.http_code = http_code
            else:
                msg = 'Can\'t find the server'

        LOGGER.debug(msg)
        self.error = msg

    @abc.abstractmethod
    def connection_finished(self):
        return

    def is_finished(self, paginated=False):
        return (self._pagination_exhausted if paginated
                else self.reply.isFinished())
