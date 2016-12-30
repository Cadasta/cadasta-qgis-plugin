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
from qgis.gui import QgsMessageBar
from cadasta.api.login import Login
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
    get_authtoken
)
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_widget_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class OptionsWidget(WidgetBase, FORM_CLASS):
    """Options widget"""

    def __init__(self, parent=None):
        """Constructor

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(OptionsWidget, self).__init__(parent)
        self.text_test_connection_button = None
        self.url = None
        self.auth_token = None
        self.login_api = None
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

        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(
            self.clear_information
        )
        self.url_input.setText(get_url_instance())

        # If login information exists
        if get_authtoken():
            self.clear_button.setEnabled(True)
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
        delete_authtoken()
        delete_setting('username')
        self.clear_button.setEnabled(False)
        self.token_status.setText(
            tr(
                'Auth token is empty.'
            )
        )
        self.parent.unauthenticated.emit()

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
            self.save_button.setEnabled(True)
            self.ok_label.setText(self.tr('Success'))
            self.ok_label.setStyleSheet('color:green')
            self.parent.authenticated.emit()
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
            self.clear_button.setEnabled(True)
            save_authtoken(self.auth_token)
            save_url_instance(self.url)
            self.parent.close()
