# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 1 : Define basic project properties

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import os
import json
from PyQt4.QtGui import QAbstractItemView, QListWidgetItem
from PyQt4.QtCore import Qt
from qgis.core import QgsVectorFileWriter
from qgis.core import QgsGeometry
from cadasta.utilities.resources import is_valid_url
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.api.organization import Organization
from cadasta.common.setting import get_path_data
from cadasta.model.contact import Contact
from qgis.gui import QgsMapLayerComboBox

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation1(WizardStep, FORM_CLASS):
    """Step 1 for project creation."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectCreation1, self).__init__(parent)
        self.organisation = Organization()
        self.get_organisation_button.clicked.connect(
            self.get_available_organisations
        )

    def set_widgets(self):
        """Set all widgets on the tab."""
        contacts = Contact.get_rows()

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

        self.project_contact_list.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

    def project_name(self):
        """Get project name from input.

        :returns: Project name
        :rtype: str
        """
        return self.project_name_text.displayText()

    def project_url(self):
        """Get project url from input.

        :returns: Project url
        :rtype: str
        """
        return self.project_url_text.displayText()

    def selected_layer(self):
        """Get selected layer from combo box.

        :returns: Layer data
        :rtype: QgsVectorLayer
        """
        layer_data = self.qgis_layer_box.currentLayer()
        return layer_data

    def selected_organisation(self):
        """Get selected organisation from combo box.

        :returns: Organisation data
        :rtype: dict
        """
        organisation_data = self.organisation_box.itemData(
            self.organisation_box.currentIndex()
        )
        return organisation_data

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        error_message = ''

        if self.project_url() and \
                not is_valid_url(self.project_url()):
            error_message = tr('Invalid url.')

        if not self.project_name() or \
                not self.selected_organisation():
            error_message = tr('Empty required field.')

        return (
            error_message == '',
            error_message
        )

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        # Check if layer has locations
        features = self.selected_layer().getFeatures()
        feature = next(features, None)
        # If no locations found, skip step 2
        if not feature:
            new_step = self.parent.step_project_creation03
        else:
            new_step = self.parent.step_project_creation02
        return new_step

    def get_available_organisations(self):
        """Get available organisations and load it to
           organisation combo box.
        """
        LOGGER.info('Getting organisations')
        self.get_organisation_button.setEnabled(False)
        status, results = self.organisation.organizations_project_filtered()
        self.get_organisation_button.setEnabled(True)
        if status:
            self.organisation_box.clear()
            self.parent.organisations_list = results
            for organisation in results:
                self.organisation_box.addItem(
                    organisation['name'],
                    organisation
                )
        else:
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr(results)
            )

    def all_data(self):
        """Return all data from this step.

        :returns: step 1 data
        :rtype: dict
        """
        data = dict()
        data['organisation'] = self.selected_organisation()
        data['project_name'] = self.project_name()
        data['project_url'] = self.project_url()
        data['description'] = self.project_description_text.toPlainText()
        data['private'] = self.is_project_private.isChecked()

        # Get contacts
        data['contacts'] = []
        contact_item_list = self.project_contact_list.selectedItems()
        for contact_item in contact_item_list:
            contact = contact_item.data(Qt.UserRole)
            data['contacts'].append({
                'name': contact.name,
                'tel': contact.phone,
                'email': contact.email
            })

        # Get extent
        layer = self.selected_layer()
        if self.use_layer_extents.isChecked():
            # Layer extent
            extent = layer.extent()
        else:
            # Canvas extent
            extent = self.parent.iface.mapCanvas().extent()

        geometry = QgsGeometry().fromRect(extent)
        data['extent'] = geometry.exportToGeoJSON()

        # Save layer to geojson format
        output_file = get_path_data(project_slug='temp_project')
        output_file = os.path.join(
            output_file,
            '%s.geojson' % 'temp_project'
        )

        result = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            output_file,
            'utf-8',
            layer.crs(),
            'GeoJson'
        )

        if result == QgsVectorFileWriter.NoError:
            LOGGER.debug('Wrote layer to geojson: %s' % output_file)
            with open(output_file) as json_data:
                layer_data = json.load(json_data)
                data['locations'] = layer_data
            os.remove(output_file)
        else:
            LOGGER.error('Failed with error: %s' % result)
        return data
