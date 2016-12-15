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
from qgis.PyQt import QtGui
from qgis.PyQt.QtNetwork import *
from qgis.PyQt.QtCore import *
from utilities.resources import get_ui_class
from source.api.login import Login

FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CadastaLogin, self).__init__(parent)
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.manager = QNetworkAccessManager()
        self.reply = QNetworkReply

    def http_finished(self):
        self.output_label.setText(str(self.reply.readAll()))
        self.loginButton.setEnabled(True)

    def login(self):
        self.loginButton.setEnabled(False)
        username = self.usernameInput.displayText()
        password = self.passwordInput.displayText()

        url = QUrl('https://platform-staging-api.cadasta.org/api/v1/account/login/?')
        req = QNetworkRequest(url)

        post_data = QByteArray()
        post_data.append("username=%s&" % username)
        post_data.append("password=%s" % password)

        self.reply = self.manager.post(req, post_data)

        self.reply.finished.connect(self.http_finished)
