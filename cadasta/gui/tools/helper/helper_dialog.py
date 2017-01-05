# coding=utf-8
"""
Cadasta **Cadasta Help Dialog.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging
from qgis.PyQt.QtGui import QDialog

from cadasta.gui.tools.helper.content.cadasta_help import cadasta_help
from cadasta.gui.tools.helper.content.options_help import options_help
from cadasta.gui.tools.helper.content.download_project_help import (
    download_project_help
)
from cadasta.gui.tools.helper.content.create_project_help import (
    create_project_help
)
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import html_header, html_footer, get_ui_class
from extras import messaging as m

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('helper_dialog.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class HelperDialog(QDialog, FORM_CLASS):
    """Helper dialog for cadasta."""

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
        self.setWindowTitle('Cadasta Helper')
        self.iface = iface
        self.close_button.clicked.connect(self.close)
        # set the helpers
        self.show_cadasta_help()

    def show_cadasta_help(self):
        """Show usage info to the user."""
        header = html_header()
        footer = html_footer()
        string = header

        # create brand
        message = m.Message()
        message.add(m.Brand())

        string += message.to_html()

        # create content sequentially
        # 1. Download Project
        # 2. Create Project
        # 3. Update Project
        message = cadasta_help()
        string += message.to_html()

        message = download_project_help()
        string += message.to_html()

        message = create_project_help()
        string += message.to_html()

        # create other helper
        # 1. Options
        # 2. Contact

        message = m.Message()
        message.add(m.Paragraph(tr(
            'There are another dialogs, which are:')))
        string += message.to_html()

        message = options_help()
        string += message.to_html()
        string += footer

        self.help_web_view.setHtml(string)
