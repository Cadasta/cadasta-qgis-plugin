# coding=utf-8
"""
Cadasta **Cadasta Dialog Base.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging
from qgis.PyQt.QtGui import (
    QDialog,
    QPixmap
)
from qgis.PyQt.QtCore import pyqtSignal

from cadasta.utilities.resources import get_ui_class, resources_path
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('dialog_base.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaDialog(QDialog, FORM_CLASS):
    """Dialog base class for cadasta."""

    authenticated = pyqtSignal()
    unauthenticated = pyqtSignal()

    def __init__(self, parent=None, iface=None,
                 title='Cadasta', subtitle='', widget=None):
        """Constructor for the dialog.

        .. note:: In QtDesigner the advanced editor's predefined keywords
           list should be shown in english always, so when adding entries to
           cboKeyword, be sure to choose :safe_qgis:`Properties<<` and untick
           the :safe_qgis:`translatable` property.

        :param parent: Parent widget of this dialog.
        :type parent: QWidget

        :param iface: QGIS QGisAppInterface instance.
        :type iface: QGisAppInterface

        :param title: Title of dialog.
        :type title: str

        :param subtitle: Subtitle of dialog.
        :type subtitle: str

        :param widget: Widget that will be rendered to dialog
        :type widget: WidgetBase
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.label_subtitle.setText(
            tr(subtitle)
        )

        self.iface = iface
        self.set_logo()
        self.widget = widget
        if self.widget:
            self.widget.parent = self
            self.socket_layout.addWidget(self.widget)

    def set_logo(self):
        """Set logo of dialog."""
        filename = resources_path('images', 'white_icon.png')
        pixmap = QPixmap(filename)
        self.label_main_icon.setPixmap(pixmap)
