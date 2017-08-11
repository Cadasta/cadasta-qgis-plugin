# coding=utf-8
"""
Cadasta Widget -**Edit Text Dialog**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import os
import logging
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import (
    QDialog,
)
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QDesktopServices
from cadasta.utilities.resources import get_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')
FORM_CLASS = get_ui_class(os.path.join(
    'utilities', 'edit_text_dialog.ui'))


class EditTextDialog(QDialog, FORM_CLASS):
    """Dialog for just contains edit text
    """
    edit_text_done = pyqtSignal()

    def __init__(self, parent=None, iface=None, text=""):
        """Constructor for the dialog.

        .. note:: In QtDesigner the advanced editor's predefined keywords
           list should be shown in english always, so when adding entries to
           cboKeyword, be sure to choose :safe_qgis:`Properties<<` and untick
           the :safe_qgis:`translatable` property.

        :param parent: Parent widget of this dialog.
        :type parent: QWidget

        :param iface: QGIS QGisAppInterface instance.
        :type iface: QGisAppInterface

        :param text: Default text to be shown
        :type text: str

        :param ok_method: Method that will be called if finished
        :type ok_method: function
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Cadasta Questionnaire')
        self.show()
        self.edit_text.setText(text)
        self.ok_button.clicked.connect(
            self.close_edit_text_dialog
        )
        self.data_schema_help.mousePressEvent = self.show_advanced_help

    def show_advanced_help(self, event):
        """Show advanced help
        """
        QDesktopServices().openUrl(
                QUrl("https://cadasta.github.io/api-docs/#questionnaires"))

    def close_edit_text_dialog(self):
        """Function that call when ok button is clicked.
        """
        self.edit_text_done.emit()
        self.close()

    def get_text(self):
        """Getting current text in edit text.

        :return: edited text
        :rtype: str
        """
        return self.edit_text.toPlainText()
