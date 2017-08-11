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
    QDialog
)
from PyQt4.QtCore import QUrl, QRegExp, Qt
from PyQt4.QtGui import QDesktopServices, QColor, QTextCharFormat, QFont, QSyntaxHighlighter
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
        self.highlighter = Highlighter(self.edit_text.document())
        self.show()
        self.edit_text.setPlainText(text)
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


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        self.highlighting_rules = []

        value_format = QTextCharFormat()
        value_format.setForeground(Qt.darkRed)
        self.highlighting_rules.append((
            QRegExp("\\btrue\\b|\\bnull\\b|\\bfalse\\b|\\b[0-9]+\\b"),
            value_format
        ))

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(Qt.darkGreen)
        self.highlighting_rules.append((QRegExp("\".*\""),
                                       quotation_format))

        self.comment_start_expression = QRegExp("/\\*")
        self.comment_end_expression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, highlight_format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, highlight_format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.indexIn(text)

        while start_index >= 0:
            end_index = self.comment_end_expression.indexIn(text, start_index)

            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + \
                                 self.comment_end_expression.matchedLength()

            start_index = self.comment_start_expression.indexIn(
                    text,
                    start_index + comment_length)
