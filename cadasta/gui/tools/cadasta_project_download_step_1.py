# -*- coding: utf-8 -*-
"""Contains project download step 1 dialog.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import logging
from qgis.gui import QgsMessageBar

from cadasta.api.organization import Organization
from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.gui.tools.cadasta_project_download_step_2 import (
    CadastaProjectDownloadStep2
)
from cadasta.utilities.resources import get_ui_class

FORM_CLASS = get_ui_class('cadasta_project_download_step_1.ui')
LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaProjectDownloadStep1(CadastaDialog, FORM_CLASS):
    """Dialog class for selecting organization."""

    def __init__(self, parent=None):
        """Constructor."""

        super(CadastaProjectDownloadStep1, self).__init__(parent)
        self.setupUi(self)
        self.message_bar = None
        self.init_style()
        self.organization_api = Organization()
        self.get_available_projects_button.clicked.connect(
            self.get_organization)
        self.step_2_button.clicked.connect(self.goto_step_2)
        self.next_button.clicked.connect(self.goto_step_2)

    def init_style(self):
        """Initiate custom style for widgets. """

        self.disable_button(self.step_1_button)
        self.enable_button(self.step_2_button)
        self.enable_button(self.next_button)
        self.enable_button(self.get_available_projects_button)

    def goto_step_2(self):
        """Go to step 2 dialog"""

        if self.project_combo_box.currentIndex() < 0:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('Organization should be selected first')
            )
        else:
            project_slug = self.project_combo_box.itemData(
                self.project_combo_box.currentIndex())
            step_2 = CadastaProjectDownloadStep2(project_slug, self)
            self.hide()
            step_2.show()
            step_2.exec_()

    def get_organization(self):
        """Get organization list """

        # call api
        self.disable_button(self.get_available_projects_button)
        organizations = self.organization_api.all_organizations()

        # call api done
        self.enable_button(self.get_available_projects_button)
        self.project_combo_box.clear()
        if organizations[0]:
            for organization in organizations[1]:
                self.project_combo_box.addItem(
                    organization['name'], organization['slug'])
