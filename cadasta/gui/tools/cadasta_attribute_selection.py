# -*- coding: utf-8 -*-
"""Contains attribute selection dialog for project creation wizard.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from qgis.gui import QgsMessageBar
from qgis.PyQt import QtGui
from cadasta.utilities.resources import get_ui_class
from cadasta.utilities.i18n import tr

FORM_CLASS = get_ui_class('cadasta_attribute_selection.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaAttributeSelection(QtGui.QDialog, FORM_CLASS):
    """Dialog to select attribute from layer."""

    def __init__(self, parent=None, iface=None):
        """Constructor for attribute selection dialog.

        :param parent: Optional widget to use as parent
        :type parent: QWidget

        :param iface: An instance of QGisInterface
        :type iface: QGisInterface
        """
        super(CadastaAttributeSelection, self).__init__(parent)
        self.setupUi(self)
        self.message_bar = None
        self.parent = parent
        self.iface = iface

        self.layer = self.parent.selected_layer()
        self.organisation = self.parent.selected_organisation()

        self.init_gui_element()

    def init_gui_element(self):
        """Init gui element (button, combo box, etc)."""
        self.next_button.clicked.connect(
            self.next_step
        )

        field_names = [field.name() for field in self.layer.pendingFields()]
        field_names.remove(u'id')
        field_names.insert(0, ' ')

        self.location_attribute_combo_box.addItems(
            field_names
        )

        self.location_type_combo_box.addItems(
            field_names
        )

        self.party_name_combo_box.addItems(
            field_names
        )

        self.relationship_type_combo_box.addItems(
            field_names
        )

        self.party_type_combo_box.addItems(
            field_names
        )

        self.party_attribute_combo_box.addItems(
            field_names
        )

        self.relationship_attribute_combo_box.addItems(
            field_names
        )

        # for elem in self.layer.getFeatures():
        #     print dict(zip(field_names, elem.attributes()))

    def next_step(self):
        """Go to the next step, check all input first."""
        pass
