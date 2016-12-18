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

from qgis.PyQt import QtGui
from qgis.gui import QgsMessageBar
from cadasta.utilities.resources import get_ui_class

from cadasta.api.login import Login

FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CadastaLogin, self).__init__(parent)
        self.setupUi(self)
        self.login_button.clicked.connect(self.login)
        self.msg_bar = None

    def login(self):
        """Login function when tools button clicked"""
        username = self.username_input.displayText()
        password = self.password_input.displayText()

        if not username or not password:
            self.msg_bar = QgsMessageBar()
            self.msg_bar.pushWarning("Error", "Username/password is empty.")
        else:
            self.login_button.setEnabled(False)
            self.output_label.setText("logging in....")
            # call tools API
            self.login_api = Login(username, password, self.on_finished)

    def on_finished(self, result):
        """On finished function when tools request is finished"""
        if 'auth_token' in result:
            auth_token = result['auth_token']
            output_result = "auth_token is %s" % auth_token
        else:
            output_result = "'%s'" % result
        self.output_label.setText(output_result)
        self.login_button.setEnabled(True)
