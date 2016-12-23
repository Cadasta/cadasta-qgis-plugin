# -*- coding: utf-8 -*-
"""Contains login dialog

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '15/12/2016'
__copyright__ = 'Copyright 2016, Cadasta'

from qgis.gui import QgsMessageBar
from cadasta.utilities.resources import get_ui_class

from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.api.login import Login
from cadasta.common.setting import save_authtoken, save_url_instance

FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(CadastaDialog, FORM_CLASS):
    def __init__(self):
        """Constructor."""

        super(CadastaLogin, self).__init__()
        self.message_bar = None
        self.text_test_connection_button = self.test_connection_button.text()
        self.ok_label.setVisible(False)
        self.init_style()

    def init_style(self):
        """Initiate custom styles for dialog. """
        self.disable_button(self.save_button)
        self.enable_button(self.test_connection_button)
        self.test_connection_button.clicked.connect(self.login)
        self.save_button.clicked.connect(self.save_authtoken)

    def login(self):
        """Login function when tools button clicked."""

        username = self.username_input.displayText()
        password = self.password_input.text()
        self.url = self.url_input.displayText()
        self.auth_token = None

        self.disable_button(self.save_button)
        self.ok_label.setVisible(False)

        if not self.url or not username or not password:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('URL/Username/password is empty.')
            )
        else:
            self.disable_button(self.test_connection_button)
            self.test_connection_button.setText(self.tr('Logging in...'))
            # call tools API
            self.login_api = Login(
                self.url,
                username,
                password,
                self.on_finished)

    def on_finished(self, result):
        """On finished function when tools request is finished."""

        self.ok_label.setVisible(True)
        if 'auth_token' in result:
            self.auth_token = result['auth_token']
            self.enable_button(self.save_button)
            self.ok_label.setText(self.tr('Success'))
            self.ok_label.setStyleSheet('color:green')
        else:
            self.disable_button(self.save_button)
            self.ok_label.setText(self.tr('Failed'))
            self.ok_label.setStyleSheet('color:red')

        self.test_connection_button.setText(self.text_test_connection_button)
        self.enable_button(self.test_connection_button)

    def save_authtoken(self):
        """Save received authtoken to setting."""

        if self.auth_token:
            save_authtoken(self.auth_token)
            save_url_instance(self.url)
            self.close()
