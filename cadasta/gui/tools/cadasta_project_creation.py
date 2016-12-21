# -*- coding: utf-8 -*-
"""Contains project creation wizard

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from qgis.gui import QgsMessageBar
from qgis.PyQt import QtGui
from cadasta.utilities.resources import get_ui_class, is_valid_url
from cadasta.utilities.i18n import tr

from cadasta.api.organization import Organization

FORM_CLASS = get_ui_class('cadasta_project_creation.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaProjectCreation(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None, iface=None):
        """Constructor for project creation dialog.

        :param parent: Optional widget to use as parent
        :type parent: QWidget

        :param iface: An instance of QGisInterface
        :type iface: QGisInterface
        """
        super(CadastaProjectCreation, self).__init__(parent)
        self.setupUi(self)
        self.message_bar = None
        self.organisations_list = None
        self.init_gui_element()
        self.form_valid_flag = False
        self.iface = iface
        self.get_available_layers()

    def init_gui_element(self):
        """Init gui element (button, combo box, etc)."""
        self.get_organisations_button.clicked.connect(
            self.get_available_organisations
        )
        self.next_button.clicked.connect(
            self.next_step
        )

    def get_available_organisations(self):
        """Get available organisations."""
        LOGGER.info('Getting organisations')
        organization = Organization()
        status, results = organization.all_organizations()
        if status:
            self.organisation_combo_box.clear()
            self.organisations_list = results
            for organisation in results:
                self.organisation_combo_box.addItem(
                    organisation['name'],
                    organisation['id']
                )
        else:
            self.message_bar.pushWarning(
                    self.tr('Error'),
                    self.tr(results)
            )

    def get_available_layers(self):
        """Get layer from qgis."""
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.qgis_layer_combo_box.addItems(layer_list)

    def next_step(self):
        """Go to the next step, check all input first."""

        message = ''

        if not self.project_url_input or \
                not is_valid_url(self.project_url_input.displayText()):
            message = tr(
                'Missing or Invalid url.'
            )

        LOGGER.info(message)

        if message:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                tr('Error'),
                message
            )
        else:
            self.form_valid_flag = True
