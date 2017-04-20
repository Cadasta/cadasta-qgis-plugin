# coding=utf-8
"""
Cadasta project update step -**Cadasta Wizard**

This module provides: Project Update Step 5 : Upload update data

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import json
from PyQt4.QtCore import Qt
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from PyQt4.QtCore import QCoreApplication
from cadasta.utilities.utilities import Utilities
from cadasta.api.api_connect import ApiConnect
from cadasta.common.setting import get_url_instance

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate03(WizardStep, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate03, self).__init__(parent)
        self.submit_button.clicked.connect(self.upload_update)
        self.project_upload_result = None
        self.current_progress = 0
        self.data = None
        self.project = None
        self.layer = None
        self.vlayers = []

        self.should_update_project = True
        self.should_update_spatial = True
        self.should_update_party = True
        self.should_update_relationship = True

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project = self.parent.project['information']
        for project_layer in self.project['layers']:
            layer = QgsMapLayerRegistry.instance().mapLayer(
                project_layer['id'])
            if layer:
                self.vlayers.append(layer)

        self.layer = self.parent.project['vector_layer']
        self.lbl_status.setText(
            self.tr('Upload the data?')
        )
        self.set_progress_bar(0)

    def set_status(self, status):
        """Show status in label and text edit.

        :param status: Given status
        :type status: str
        """
        self.lbl_status.setText(status)
        self.text_edit.append(status + '\n')

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return None

    def set_progress_bar(self, value):
        """Set progress bar value.

        :param value: integer value for progress bar
        :type value: int
        """
        self.progress_bar.setValue(value)
        QCoreApplication.processEvents()

    def update_project(self):
        """Update a basic project information in an organization."""
        step2 = self.parent.step_project_update02

        contact_item_list = step2.project_contact_list.selectedItems()
        contacts = []
        for contact_item in contact_item_list:
            contact = contact_item.data(Qt.UserRole)
            contacts.append({
                'name': contact.name,
                'tel': contact.phone,
                'email': contact.email
            })

        access = 'private' if step2.access_checkbox.isChecked() else 'public'
        post_data = {
            'name': step2.project_name_text.displayText(),
            'description': step2.project_desc_text.toPlainText(),
            'urls': [
                step2.project_url_text.displayText()
            ],
            'access': access,
            'contacts': contacts
        }

        status, response = step2.send_update_request(post_data)
        if status:
            Utilities.update_project_basic_information(
                information=response,
                vlayers=self.vlayers
            )
            self.set_status(
                self.tr('Update success')
            )
        else:
            self.set_status(
                Utilities.extract_error_detail(response)
            )

    def update_spatial_location(self):
        """Update spatial information."""
        update_loc_api = '/api/v1/organizations/{organization_slug}/' \
                         'projects/{project_slug}/spatial/{spatial_unit_id}/'

        location_type_idx = self.layer.fieldNameIndex('type')
        location_id_idx = self.layer.fieldNameIndex('id')

        for layer in self.vlayers:
            features = layer.getFeatures()

            for feature in features:
                attributes = feature.attributes()
                api = update_loc_api.format(
                    organization_slug=self.project['organization']['slug'],
                    project_slug=self.project['slug'],
                    spatial_unit_id=attributes[location_id_idx]
                )

                if attributes[location_id_idx]:
                    geojson = feature.geometry().exportToGeoJSON()
                    self.upload_update_locations(
                        api,
                        geojson,
                        attributes[location_type_idx]
                    )
                if not attributes[location_id_idx]:
                    # New location
                    geojson = feature.geometry().exportToGeoJSON()
                    project_id = self.add_new_locations(
                        geojson,
                        attributes[location_type_idx]
                    )
                    layer.startEditing()
                    layer.changeAttributeValue(
                        feature.id(), 1, project_id
                    )
                    layer.commitChanges()

    def update_relationship_attributes(self):
        """Update relationship attribute for location"""
        if 'relationship_layer_id' not in self.project:
            return

        relationship_id = self.project['relationship_layer_id']

        if not relationship_id:
            return

        relationship_layer = QgsMapLayerRegistry.instance().mapLayer(
            relationship_id
        )
        if not relationship_layer:
            return

        relationship_feats = relationship_layer.getFeatures()
        relationship_id_idx = 1
        relationship_type_idx = 2
        attributes_idx = 4

        update_api = '/api/v1/organizations/{organization_slug}/projects/' \
                     '{project_slug}/relationships/tenure/{relationship_id}/'

        field_names = [
            field.name() for field in relationship_layer.pendingFields()
        ]

        # Remove unneeded fields
        field_names.remove('spatial_id')
        field_names.remove('rel_id')
        field_names.remove('rel_name')
        field_names.remove('party_id')

        for feature in relationship_feats:
            attributes = feature.attributes()
            api = update_api.format(
                organization_slug=self.project['organization']['slug'],
                project_slug=self.project['slug'],
                relationship_id=attributes[relationship_id_idx]
            )

            # Check if there are questionnaire attributes
            questionnaire_attributes = dict()
            for field_name in field_names:
                index = relationship_layer.fieldNameIndex(field_name)
                if index == -1:
                    continue
                questionnaire = attributes[index]
                if questionnaire and questionnaire != '-':
                    questionnaire_attributes[field_name] = questionnaire

            self.upload_relationship(
                api,
                attributes[relationship_type_idx],
                questionnaire_attributes
            )

    def update_party_attributes(self):
        """Update party attribute for this project."""
        information = Utilities.get_basic_information_by_vector(self.layer)

        if not information:
            return

        if 'party_layer_id' not in information:
            return

        party_id = information['party_layer_id']

        party_layer = QgsMapLayerRegistry.instance().mapLayer(party_id)
        if not party_layer:
            return

        party_feats = party_layer.getFeatures()
        id_idx = 0
        name_idx = 1
        type_idx = 2

        update_api = '/api/v1/organizations/{organization_slug}/projects/' \
                     '{project_slug}/parties/{party_id}/'

        # Remove unneeded fields
        field_names = [field.name() for field in party_layer.pendingFields()]
        field_names.remove('id')
        field_names.remove('name')
        field_names.remove('type')

        for feature in party_feats:
            attributes = feature.attributes()
            api = update_api.format(
                organization_slug=self.project['organization']['slug'],
                project_slug=self.project['slug'],
                party_id=attributes[id_idx]
            )

            # Check if there are questionnaire attributes
            questionnaire_attributes = dict()
            for field_name in field_names:
                index = party_layer.fieldNameIndex(field_name)
                if index == -1:
                    continue
                questionnaire = attributes[index]
                if questionnaire and questionnaire != '-':
                    questionnaire_attributes[field_name] = questionnaire

            self.upload_parties(
                api,
                attributes[name_idx],
                attributes[type_idx],
                questionnaire_attributes
            )

    def upload_update(self):
        """Upload the updates"""
        self.progress_bar.setVisible(True)
        self.submit_button.setVisible(False)
        self.parent.back_button.setEnabled(False)

        if self.should_update_project:
            self.set_status(
                self.tr('Update project information')
            )
            self.update_project()
            self.set_progress_bar(25)
            self.set_status(
                self.tr('Finished update project information')
            )

        if self.should_update_spatial:
            self.set_status(
                self.tr('Update spatial information')
            )
            self.set_progress_bar(50)
            self.update_spatial_location()
            self.set_status(
                self.tr('Finished update locations')
            )

        if self.should_update_relationship:
            self.set_status(
                self.tr('Update relationship')
            )
            self.set_progress_bar(60)
            self.update_relationship_attributes()
            self.set_status(
                self.tr('Finished update relationship')
            )

        if self.should_update_party:
            self.set_status(
                self.tr('Update parties')
            )
            self.set_progress_bar(80)
            self.update_party_attributes()
            self.set_status(
                self.tr('Finished update party')
            )

        self.set_progress_bar(100)

    def upload_update_locations(self, api, geometry, location_type):
        """Upload update location data.

        :param api: Api url to upload location
        :type api: str

        :param geometry: Location geojson geometry
        :type geometry: str

        :param location_type: Location type
        :type location_type: str
        """
        post_data = {
            'geometry': geometry,
            'type': location_type
        }

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.patch_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Location updated.')
            )
        else:
            self.set_status(
                Utilities.extract_error_detail(result)
            )

    def add_new_locations(self, geometry, location_type):
        """Add new location

        :param geometry: Location geojson geometry
        :type geometry: str

        :param location_type: Location type
        :type location_type: str
        """
        api = '/api/v1/organizations/{organization_slug}/projects/' \
              '{project_slug}/spatial/'.format(
                organization_slug=self.project['organization']['slug'],
                project_slug=self.project['slug'])

        post_data = {
            'geometry': geometry
        }

        if location_type:
            post_data['type'] = location_type

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.post_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Location added.')
            )
            return json.loads(result)['properties']['id']
        else:
            self.set_status(
                Utilities.extract_error_detail(result)
            )
            return None

    def upload_parties(self, api, party_name, party_type, attributes=None):
        """Upload party data.

        :param api: Api url to upload party
        :type api: str

        :param party_name: Party name
        :type party_name: str

        :param party_type: Party type
        :type party_type: str

        :param attributes: Project-specific attributes that are defined
                           through the project's questionnaire
        :type attributes: dict
        """
        post_data = {
            'name': party_name,
            'type': party_type
        }

        if attributes:
            post_data['attributes'] = attributes

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.patch_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Party updated.')
            )
        else:
            self.set_status(
                Utilities.extract_error_detail(result)
            )

    def upload_relationship(self, api, relationship_type, attributes=None):
        """Upload relationship data.

        :param api: Api url to upload party
        :type api: str

        :param relationship_type: Relationship type
        :type relationship_type: str

        :param attributes: Project-specific attributes that are defined
                           through the project's questionnaire
        :type attributes: str
        """
        post_data = {
            'tenure_type': relationship_type,
        }

        if attributes:
            post_data['attributes'] = attributes

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.patch_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Relationship updated.')
            )
        else:
            self.set_status(
                Utilities.extract_error_detail(result)
            )
