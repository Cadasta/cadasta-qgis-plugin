# coding=utf-8
"""
Cadasta Contact -**Cadasta Widget**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import re

from qgis.gui import QgsMessageBar
from qgis.PyQt.QtGui import (
    QHeaderView,
    QAbstractItemView
)
from cadasta.gui.tools.widget.widget_base import (
    get_widget_step_ui_class,
    WidgetBase
)
from cadasta.model.contact import Contact

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_widget_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ContactWidget(WidgetBase, FORM_CLASS):
    """Contact widget."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(ContactWidget, self).__init__(parent)
        # Create model
        self.model = Contact.table_model()
        self.set_widgets()

    def set_widgets(self):
        """Set all widgets."""
        self.contact_listview.horizontalHeader().setStretchLastSection(True)
        self.contact_listview.horizontalHeader().setResizeMode(
            QHeaderView.Stretch)
        self.contact_listview.setModel(self.model)
        self.contact_listview.hideColumn(0)
        self.contact_listview.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.add_button.clicked.connect(self.add_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.save_button.clicked.connect(self.save_model)

    def add_contact(self):
        """Add contact."""
        row = self.model.rowCount()
        self.model.insertRows(row, 1)

    def delete_contact(self):
        """Delete contact."""
        self.model.removeRows(self.contact_listview.currentIndex().row(), 1)

    def validate_email(self, email):
        """Delete email.

        :param email: email that will be checked.
        :type email: str

        :return: boolean is validated or not
        :rtype: bool
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def save_model(self):
        """Save model contact."""
        error = None
        for i in xrange(self.model.rowCount()):
            record = self.model.record(i)
            if not record.value("email") and not record.value("phone"):
                error = self.tr(
                    'One or more contact doesn\'t has email and '
                    'phone. Either email or phone must be provided.')
                break
                # validate email
            if record.value("email") and not self.validate_email(
                    record.value("email")):
                error = self.tr(
                    'There is one or more wrong email in contact ist.')

        if not error:
            self.model.submitAll()
        else:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                error
            )
