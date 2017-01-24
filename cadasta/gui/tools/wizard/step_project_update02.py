# coding=utf-8
"""
Cadasta project update step -**Cadasta Wizard**

This module provides: Project Update Step 2 : Project basic information

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import json
from qgis.PyQt.QtGui import QAbstractItemView, QListWidgetItem
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import QCoreApplication
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.model.contact import Contact
from cadasta.mixin.network_mixin import NetworkMixin
from cadasta.common.setting import get_url_instance

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate02(WizardStep, FORM_CLASS):
    """Step 1 for project update."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate02, self).__init__(parent)
        self.parent = parent
        self.project = None
        self.update_button.clicked.connect(self.update_project)

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project = self.parent.project

        self.update_status_label.setText('')

        self.project_name_text.setText(self.project['name'])

        if self.project['urls']:
            self.project_url_text.setText(self.project['urls'][0])
        else:
            self.project_url_text.setText('')

        self.project_desc_text.setText(self.project['description'])

        if self.project['access'] == 'private':
            private_access = True
        else:
            private_access = False
        self.access_checkbox.setChecked(private_access)

        contacts = Contact.get_rows()
        project_contacts = self.project['contacts']

        self.project_contact_list.clear()
        self.project_contact_list.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        # From local db
        for contact in contacts:
            contact_name = contact.name
            contact_email = ' - ' + contact.email if contact.email else ''
            contact_phone = ' - ' + contact.phone if contact.phone else ''

            contact_item = QListWidgetItem(
                contact_name + contact_email + contact_phone
            )

            contact_item.setData(Qt.UserRole, contact)
            self.project_contact_list.addItem(
                contact_item
            )

        # From server
        for index, contact in enumerate(project_contacts):
            contact_name = contact['name']
            contact_email = ' - ' + contact['email'] \
                if contact['email'] else ''
            contact_phone = ' - ' + contact['tel'] if contact['tel'] else ''

            contact_box = self.project_contact_list.findItems(
                contact_name + contact_email + contact_phone,
                Qt.MatchExactly
            )

            if len(contact_box) > 0:
                contact_box[0].setSelected(True)
            else:
                new_contact = Contact()
                new_contact.name = contact['name']
                new_contact.email = contact['email']
                new_contact.phone = contact['tel']
                new_contact.save()

                selected_item = QListWidgetItem(
                    contact_name + contact_email + contact_phone
                )
                selected_item.setData(Qt.UserRole, new_contact)

                self.project_contact_list.addItem(
                    selected_item
                )

                selected_item.setSelected(True)

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return self.parent.step_project_update03

    def send_update_request(self, post_data):
        """Send update request to server and return the responses

        :param post_data: Data to post
        :type post_data: json string

        :returns: Tuple of request status and error message
        :rtype: ( bool, str )
        """
        update_url = '/api/v1/organizations/%s/projects/%s/' % (
            self.project['organization']['slug'],
            self.project['slug']
        )
        network = NetworkMixin(get_url_instance() + update_url)
        network.connect_json_patch(json.dumps(post_data))
        while not network.reply.isFinished():
            QCoreApplication.processEvents()

        if not network.error:
            return True, ''
        else:
            return False, network.results.data()

    def update_project(self):
        """Update a basic project information in an organization."""
        self.update_button.setText(
            tr('Updating')
        )
        self.update_button.setEnabled(False)

        contact_item_list = self.project_contact_list.selectedItems()
        contacts = []
        for contact_item in contact_item_list:
            contact = contact_item.data(Qt.UserRole)
            contacts.append({
                'name': contact.name,
                'tel': contact.phone,
                'email': contact.email
            })

        access = 'private' if self.access_checkbox.isChecked() else 'public'
        post_data = {
            'name': self.project_name_text.displayText(),
            'description': self.project_desc_text.toPlainText(),
            'urls': [
                self.project_url_text.displayText()
            ],
            'access': access,
            'contacts': contacts
        }

        status, message = self.send_update_request(post_data)

        self.update_button.setText(
            tr('Update')
        )
        self.update_button.setEnabled(True)

        if status:
            self.update_status_label.setText(
                tr('Update success')
            )
        else:
            self.update_status_label.setText(
                'Error: %s' % message
            )
