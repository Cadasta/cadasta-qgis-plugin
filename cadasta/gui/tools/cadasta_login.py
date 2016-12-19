# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CadastaDialog
                                 A QGIS plugin
 This tool helps create, update, upload and download Cadasta projects.
                             -------------------
        begin                : 2016-11-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Kartoza
        email                : christian@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import logging
from qgis.PyQt import QtGui
from qgis.gui import QgsMessageBar
from cadasta.utilities.resources import get_ui_class, get_project_path

from cadasta.api.login import Login
from cadasta.gui.tools.cadasta_style import CadastaStyle

LOGGER = logging.getLogger('CadastaQGISPlugin')
FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CadastaLogin, self).__init__(parent)
        self.setupUi(self)
        self.msg_bar = None
        self.text_test_connection_button = self.test_connection_button.text()
        self.ok_label.setVisible(False)
        self.init_style()

    def init_style(self):
        """
        Initiate custom styles for dialog
        """
        self.setStyleSheet("background-color:white")
        self.disable_button(self.save_button)
        self.enable_button(self.test_connection_button)
        self.test_connection_button.clicked.connect(self.login)
        self.save_button.clicked.connect(self.save_authtoken)

    def enable_button(self, custom_button):
        """
        Enable button
        :param custom_button: button that is enabled
        :type custom_button: QWidget
        """
        custom_button.setEnabled(True)
        custom_button.setStyleSheet("background-color:#525252; cursor:pointer;" + CadastaStyle.button_style())

    def disable_button(self, custom_button):
        """
        Disable button
        :param custom_button: button that is enabled
        :type custom_button: QWidget
        """
        custom_button.setStyleSheet("background-color:#A8A8A8;" + CadastaStyle.button_style())
        custom_button.setEnabled(False)

    def login(self):
        """Login function when tools button clicked"""
        username = self.username_input.displayText()
        password = self.password_input.text()
        url = self.url_input.displayText()
        self.auth_token = None

        self.disable_button(self.save_button)
        self.ok_label.setVisible(False)

        if not url or not username or not password:
            self.msg_bar = QgsMessageBar()
            self.msg_bar.pushWarning("Error", self.tr("URL/Username/password is empty."))
        else:
            self.disable_button(self.test_connection_button)
            self.test_connection_button.setText(self.tr("Logging in..."))
            # call tools API
            self.login_api = Login(url, username, password, self.on_finished)

    def on_finished(self, result):
        """On finished function when tools request is finished"""
        self.ok_label.setVisible(True)
        if 'auth_token' in result:
            self.auth_token = result['auth_token']
            self.enable_button(self.save_button)
            self.ok_label.setText(self.tr("Success"))
            self.ok_label.setStyleSheet("color:green")
        else:
            self.disable_button(self.save_button)
            self.ok_label.setText(self.tr("Failed"))
            self.ok_label.setStyleSheet("color:red")

        self.test_connection_button.setText(self.text_test_connection_button)
        self.enable_button(self.test_connection_button)

    def save_authtoken(self):
        """
        Save received authtoken to external file
        """
        if self.auth_token:
            path = get_project_path()
            filename = os.path.join(
                path,
                'secret/authtoken.txt'''
            )
            file_ = open(filename, 'w')
            file_.write(self.auth_token)
            file_.close()
            self.close()
