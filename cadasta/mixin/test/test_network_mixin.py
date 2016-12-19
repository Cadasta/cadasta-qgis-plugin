# coding=utf-8
"""
Test for network mixin connect

"""

__author__ = 'dimas.ciputra@gmail.com'
__date__ = '16/12/2016'

import unittest
import qgis
import logging
from qgis.PyQt.QtCore import QCoreApplication, QByteArray
from cadasta.mixin.network_mixin import NetworkMixin


LOGGER = logging.getLogger('CadastaQGISPlugin')


class NetworkMixinText(unittest.TestCase):
    """Test NetworkMixin class"""
    # Fake online rest api provided by http://jsonplaceholder.typicode.com

    def setUp(self):
        """Test setup."""
        self.api_results = {
            'userId': 1,
            'title': 'foo',
            'body': 'bar'
        }

    def test_network_mixin_get(self):
        """Test network mixin get"""
        request_url = 'http://jsonplaceholder.typicode.com/posts/1'
        manager = NetworkMixin(request_url=request_url)
        manager.connect_get()
        while not manager.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(manager.get_json_results())
        self.assertEqual(
                manager.get_json_results()['userId'],
                self.api_results['userId'])

    def test_network_mixin_post(self):
        """Test network mixin post"""
        request_url = 'http://jsonplaceholder.typicode.com/posts'

        post_data = QByteArray()
        post_data.append("title=%s&" % self.api_results['title'])
        post_data.append("body=%s&" % self.api_results['body'])
        post_data.append("userId=%d&" % self.api_results['userId'])

        manager = NetworkMixin(request_url=request_url)
        manager.connect_post(post_data)
        while not manager.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(manager.get_json_results())
        self.assertEqual(
                manager.get_json_results()['userId'],
                self.api_results['userId']
        )
        self.assertEqual(
                manager.get_json_results()['body'],
                self.api_results['body']
        )
