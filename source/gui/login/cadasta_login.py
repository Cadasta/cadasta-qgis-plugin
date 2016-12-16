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
from utilities.resources import get_ui_class

from source.api.login import Login

FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CadastaLogin, self).__init__(parent)
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        """Login function when login button clicked"""
        self.loginButton.setEnabled(False)
        self.output_label.setText("logging in....")
        username = self.usernameInput.displayText()
        password = self.passwordInput.displayText()

        # call login API
        self.login_api = Login(username, password, self.on_finished)

    def on_finished(self, result):
        """On finished function when login request is finished"""
        if 'auth_token' in result:
            auth_token = result['auth_token']
            output_result = "auth_token is %s" % auth_token
        else:
            output_result = "'%s'" % result
        self.output_label.setText(output_result)
        self.loginButton.setEnabled(True)
