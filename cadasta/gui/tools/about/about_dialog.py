# coding=utf-8
"""
Cadasta **Cadasta About Dialog.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from cadasta.gui.tools.about.content.about import about
from cadasta.gui.tools.about.content.overview import overview
from cadasta.gui.tools.about.content.version import version
from cadasta.gui.tools.about.content.license import license_about
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import (
    html_header,
    html_footer,
    get_ui_class,
    get_plugin_version
)
from extras import messaging as m


__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('helper_dialog.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class AboutDialog(QDialog, FORM_CLASS):
    """About dialog for cadasta."""

    def __init__(self, parent=None, iface=None):
        """Constructor for the dialog.

        .. note:: In QtDesigner the advanced editor's predefined keywords
           list should be shown in english always, so when adding entries to
           cboKeyword, be sure to choose :safe_qgis:`Properties<<` and untick
           the :safe_qgis:`translatable` property.

        :param parent: Parent widget of this dialog.
        :type parent: QWidget

        :param iface: QGIS QGisAppInterface instance.
        :type iface: QGisAppInterface
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle(tr('About Cadasta %s' % get_plugin_version()))
        self.iface = iface
        # set the helpers
        self.show_cadasta_about()

    def show_cadasta_about(self):
        """Show usage info to the user."""
        header = html_header()
        footer = html_footer()
        string = header

        # create brand
        message = m.Message()
        message.add(m.Brand())

        string += message.to_html()

        message = about()

        string += message.to_html()

        message = overview()

        string += message.to_html()

        message = version()
        string += message.to_html()

        message = license_about()
        string += message.to_html()

        string += footer

        self.help_web_view.setHtml(string)

    # prevents actions being handled twice
    # noinspection PyPep8Naming
    @pyqtSignature('')
    def on_close_button_released(self):
        """Handle the Close button release.

        .. note:: This is an automatic Qt slot
           executed when the Back button is released.
        """
        self.close()
