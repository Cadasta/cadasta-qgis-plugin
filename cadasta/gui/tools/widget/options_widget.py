# coding=utf-8
"""
Cadasta Options -**Cadasta Widget**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from PyQt4.QtCore import pyqtSignal

from qgis.gui import QgsMessageBar
from cadasta.api.login import Login
from cadasta.api.organization import Organization
from cadasta.gui.tools.widget.widget_base import (
    get_widget_step_ui_class,
    WidgetBase
)
from cadasta.common.setting import (
    save_authtoken,
    save_url_instance,
    get_url_instance,
    set_setting,
    get_setting,
    delete_authtoken,
    delete_setting,
    get_authtoken,
    save_user_organizations
)
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_widget_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class OptionsWidget(WidgetBase, FORM_CLASS):
    """Options widget."""

    authenticated = pyqtSignal()
    unauthenticated = pyqtSignal()

    def __init__(self, parent=None, auth_token=None):
        """Constructor

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(OptionsWidget, self).__init__(parent)
        self.text_test_connection_button = None
        self.url = None
        self.auth_token = auth_token
        self.login_api = None
        self.organisation_api = Organization()
        self.set_widgets()

    def set_widgets(self):
        """Set all widgets."""
        self.text_test_connection_button = self.test_connection_button.text()
        self.ok_label.setVisible(False)
        self.save_button.setEnabled(False)

        self.test_connection_button.clicked.connect(
            self.login
        )
        self.save_button.clicked.connect(
            self.save_authtoken
        )
        self.clear_button.setText(
            tr('Clear')
        )

        self.clear_button.setEnabled(True)
        self.clear_button.clicked.connect(
            self.clear_information
        )
        self.url_input.setText(get_url_instance())

        # If login information exists
        if not self.auth_token:
            self.auth_token = get_authtoken()

        if self.auth_token:
            self.test_connection_button.setEnabled(False)
            self.username_input.setText(get_setting('username'))
            self.token_status.setText(
                tr('Auth token is saved.')
            )
        else:
            self.token_status.setText(
                tr('Auth token is empty.')
            )

    def clear_information(self):
        """Clear login information."""
        self.username_input.clear()
        self.password_input.clear()
        self.ok_label.clear()
        delete_authtoken()
        delete_setting('username')
        self.test_connection_button.setEnabled(True)
        self.token_status.setText(
            tr(
                'Auth token is empty.'
            )
        )
        self.unauthenticated.emit()

    def login(self):
        """Login function when tools button clicked."""
        self.clear_button.setEnabled(False)
        username = self.username_input.displayText()
        password = self.password_input.text()
        self.url = self.url_input.displayText()
        self.auth_token = None

        self.save_button.setEnabled(False)
        self.ok_label.setVisible(False)

        if not self.url or not username or not password:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('URL/Username/password is empty.')
            )
        else:
            self.test_connection_button.setEnabled(False)
            self.test_connection_button.setText(self.tr('Logging in...'))
            # call tools API
            self.login_api = self.call_login_api(
                self.url,
                username,
                password)
            self.login_api.connect_post(self.login_api.post_data)

    def call_login_api(self, url, username, password):
        """Call login api.

        :param url: platform url
        :type url: str

        :param username: username for login
        :type username: str

        :param password: password for login
        :type password: str
        """
        return Login(
            domain=url,
            username=username,
            password=password,
            on_finished=self.on_finished
        )

    def on_finished(self, result):
        """On finished function when tools request is finished."""

        self.ok_label.setVisible(True)
        self.clear_button.setEnabled(True)
        if 'auth_token' in result:
            self.auth_token = result['auth_token']
            self.save_button.setEnabled(True)
            self.ok_label.setText(self.tr('Success'))
            self.ok_label.setStyleSheet('color:green')
        else:
            self.save_button.setEnabled(False)
            self.ok_label.setText(self.tr('Failed'))
            self.ok_label.setStyleSheet('color:red')

        self.test_connection_button.setText(self.text_test_connection_button)
        self.test_connection_button.setEnabled(True)

    def save_authtoken(self):
        """Save received authtoken to setting.

        Authoken is saved to setting, and close dialog after that.
        """

        if self.auth_token:
            set_setting('username', self.username_input.displayText())
            save_authtoken(self.auth_token)
            save_url_instance(self.url)
            self.save_button.setEnabled(False)
            self.save_organizations()

    def save_organizations(self):
        """Save organizations of user.

        Organization is saved to setting.
        If it is success, close dialog after
        that.
        """
        status, results = self.organisation_api. \
            organizations_project_filtered()
        self.clear_button.setEnabled(True)
        self.save_button.setEnabled(False)
        if status:
            organization = []
            for result in results:
                organization.append(result['slug'])
            save_user_organizations(organization)
            self.parent.close()
        else:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('Error when getting user permission.')
            )
        self.authenticated.emit()
