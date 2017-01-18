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
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from qgis.PyQt.QtCore import QCoreApplication, QByteArray
from cadasta.api.api_connect import ApiConnect
from cadasta.common.setting import get_url_instance

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate05(WizardStep, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate05, self).__init__(parent)
        self.submit_button.clicked.connect(self.upload_update)
        self.project_upload_result = None
        self.current_progress = 0
        self.data = None
        self.project = None
        self.layer = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project = self.parent.project
        self.layer = self.parent.layer
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

    def upload_update(self):
        """Upload the updates"""
        self.progress_bar.setVisible(True)
        self.submit_button.setVisible(False)
        self.parent.back_button.setEnabled(False)

        self.set_status(
            self.tr('Update locations')
        )

        fields = self.parent.get_mapped_fields()
        update_loc_api = '/api/v1/organizations/{organization_slug}/projects/{project_slug}/' \
                         'spatial/{spatial_unit_id}/'

        self.set_progress_bar(25)

        for loc in self.parent.locations['features']:
            api = update_loc_api.format(
                organization_slug=self.project['organization']['slug'],
                project_slug=self.project['slug'],
                spatial_unit_id=loc['properties']['id']
            )

            loc_type_field = fields['location_type']
            loc_type_idx = self.layer.fieldNameIndex(loc_type_field)
            loc_id_idx = self.layer.fieldNameIndex('id')

            features = self.layer.getFeatures()

            for feat in features:
                attributes = feat.attributes()
                if attributes[loc_id_idx] == loc['properties']['id']:
                    geojson = feat.geometry().exportToGeoJSON()
                    self.upload_locations(api, geojson, attributes[loc_type_idx])

        self.set_progress_bar(50)

        self.set_status(
            self.tr('Finished update locations')
        )

        # Update parties

        self.set_status(
            self.tr('Update parties')
        )

        update_api = '/api/v1/organizations/{organization_slug}/projects/{project_slug}/' \
                     'parties/{party_id}/'

        for party in self.parent.parties:
            api = update_api.format(
                organization_slug=self.project['organization']['slug'],
                project_slug=self.project['slug'],
                party_id=party['id']
            )

            party_type_field = fields['party_type']
            party_type_idx = self.layer.fieldNameIndex(party_type_field)
            party_name_field = fields['party_name']
            party_name_idx = self.layer.fieldNameIndex(party_name_field)
            party_id_idx = self.layer.fieldNameIndex('party_id')

            features = self.layer.getFeatures()

            for feat in features:
                attributes = feat.attributes()
                if attributes[party_id_idx] == party['id']:
                    self.upload_parties(api, attributes[party_name_idx], attributes[party_type_idx])

        self.set_progress_bar(100)

        self.set_status(
            self.tr('Finished update parties')
        )

    def upload_locations(self, api, geometry, location_type):
        """Upload location data.

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

        LOGGER.debug(post_data)

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.patch_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Location updated.')
            )
        else:
            self.set_progress_bar(0)
            self.set_status(
                'Error: %s' % result
            )

    def upload_parties(self, api, party_name, party_type):
        """Upload party data.

        :param api: Api url to upload party
        :type api: str

        :param party_name: Party name
        :type party_name: str

        :param party_type: Party type
        :type party_type: str
        """
        post_data = {
            'name': party_name,
            'type': party_type
        }

        LOGGER.debug(post_data)

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.patch_json(json.dumps(post_data))

        if status:
            self.set_status(
                self.tr('Party updated.')
            )
        else:
            self.set_progress_bar(0)
            self.set_status(
                'Error: %s' % result
            )
