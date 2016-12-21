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
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import logging
from qgis.PyQt import QtGui

from cadasta.gui.tools.cadasta_style import CadastaStyle

LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaDialog(QtGui.QDialog):
    """ Parent class for cadasta dialog."""

    def __init__(self, parent=None):
        """ Constructor."""

        super(CadastaDialog, self).__init__(parent)
        self.setupUi(self)
        self.message_bar = None
        self.init_style()

    def init_style(self):
        """ Initiate custom styles for dialog. """

        self.setStyleSheet('background-color:white')

    def enable_button(self, custom_button):
        """ Enable button.

        :param custom_button: button that is enabled
        :type custom_button: QWidget
        """

        custom_button.setEnabled(True)
        custom_button.setStyleSheet(
            'background-color:#525252; cursor:pointer;' +
            CadastaStyle.button_style()
        )

    def disable_button(self, custom_button):
        """ Disable button.

        :param custom_button: button that is enabled
        :type custom_button: QWidget
        """
        custom_button.setStyleSheet(
            'background-color:#A8A8A8;' + CadastaStyle.button_style()
        )
        custom_button.setEnabled(False)
