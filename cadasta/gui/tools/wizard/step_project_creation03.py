# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 3 : Upload to cadasta

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import json
import logging
from qgis.PyQt.QtCore import QCoreApplication, QByteArray
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.common.setting import get_url_instance
from cadasta.api.api_connect import ApiConnect

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation3(WizardStep, FORM_CLASS):
    """Step 3 for project creation."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectCreation3, self).__init__(parent)
        self.submit_button.clicked.connect(self.processing_data)
        self.project_upload_result = None
        self.current_progress = 0
        self.data = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.progress_bar.setVisible(False)
        self.lbl_status.setText(
            tr('Are you sure to upload the data?')
        )

    def set_status(self, status):
        """Show status in label and text edit.

        :param status: Given status
        :type status: str
        """
        self.lbl_status.setText(status)
        self.text_edit.append(status + '\n')

    def set_progress_bar(self, value):
        """Set progress bar value.

        :param value: integer value for progress bar
        :type value: int
        """
        self.progress_bar.setValue(value)
        QCoreApplication.processEvents()

    def processing_data(self):
        """Processing data from all step"""
        self.progress_bar.setVisible(True)
        self.submit_button.setVisible(False)
        self.parent.back_button.setEnabled(False)

        self.set_status(
            tr('Processing data')
        )

        self.set_progress_bar(self.current_progress + 25)

        step_1_data = self.parent.step_1_data()
        self.set_progress_bar(self.current_progress + 25)

        step_2_data = self.parent.step_2_data()
        self.set_progress_bar(self.current_progress + 25)

        self.data = step_1_data

        # Finalize the data
        for location in self.data['locations']['features']:
            for cadasta_field, layer_field in step_2_data.iteritems():
                properties = location['properties']
                if layer_field in properties:
                    try:
                        location['fields']
                    except KeyError:
                        location['fields'] = dict()
                    location['fields'][cadasta_field] = properties[
                        layer_field]
        self.set_progress_bar(100)

        self.set_status(
            tr('Finished processing data')
        )

        # Upload project
        self.upload_project()

    def upload_project(self):
        """Upload project to cadasta."""
        self.set_status(
            tr('Uploading project')
        )
        self.current_progress = 0
        self.set_progress_bar(self.current_progress)

        post_data = {
            'name': self.data['project_name'],
            'description': self.data['description'],
            'extent': self.data['extent'],
            'urls': [
                self.data['project_url']
            ],
            'access': 'private' if self.data['private'] else 'public',
            'contacts': self.data['contacts']
        }

        post_url = '/api/v1/organizations/%s/projects/' % (
            self.data['organisation']['slug']
        )

        connector = ApiConnect(get_url_instance() + post_url)
        status, result = self._call_json_post(connector, json.dumps(post_data))

        self.set_progress_bar(self.current_progress + 25)
        self.set_status(
            tr('Finished uploading project')
        )

        if status:
            self.project_upload_result = json.loads(result)
            total_locations = len(self.data['locations']['features'])
            if total_locations > 0:
                self.upload_locations()
                self.upload_parties()
                self.upload_relationships()
            self.set_progress_bar(100)
        else:
            self.set_progress_bar(0)
            self.set_status(
                'Error: %s' % result
            )

        self.set_status(tr('Finished'))

    def upload_locations(self):
        """Upload project locations to cadasta."""
        self.set_status(
            tr('Uploading locations')
        )
        total_locations = len(self.data['locations']['features'])
        progress_left = (100 - self.current_progress) / total_locations

        post_url = '/api/v1/organizations/%s/projects/%s/spatial/' % (
            self.data['organisation']['slug'],
            self.project_upload_result['slug']
        )

        failed = 0

        for location in self.data['locations']['features']:
            post_data = QByteArray()
            post_data.append(
                'geometry=%s&' % json.dumps(location['geometry']))
            post_data.append('type=%s' % location['fields']['location_type'])

            connector = ApiConnect(get_url_instance() + post_url)
            status, result = self._call_post(connector, post_data)

            if status:
                self.set_progress_bar(self.current_progress + progress_left)
                try:
                    result_obj = json.loads(result)
                    if 'properties' in result_obj:
                        location['spatial_id'] = result_obj['properties']['id']
                except ValueError as e:
                    LOGGER.exception('message')
            else:
                self.set_progress_bar(0)
                self.set_status(
                    'Error: %s' % result
                )
                failed += 1

        self.set_progress_bar(100)

        if failed == 0:
            self.set_status(
                tr('Finished uploading all locations')
            )
        else:
            self.set_status(
                tr('Finish with %d failed' % failed)
            )

    def _url_post_parties(self):
        """Get url to create a new party.

        :return: Api url or none if project_upload_result is empty
        :rtype: str, None
        """
        organisation = self.data['organisation']['slug']

        if self.project_upload_result:
            project = self.project_upload_result['slug']
            return '/api/v1/organizations/%s/projects/%s/parties/' % (
                organisation,
                project
            )
        else:
            return None

    def _url_post_relationships(self):
        """Get url to create a new relationship.

        :return: Api url or none if project_upload_result is empty
        :rtype: str, None
        """
        organisation = self.data['organisation']['slug']
        url = '/api/v1/organizations/%s/projects/%s/relationships/tenure/'

        if self.project_upload_result:
            project = self.project_upload_result['slug']
            return url % (
                organisation,
                project
            )
        else:
            return None

    def upload_parties(self):
        """Upload party from this project."""
        self.set_status(
            tr('Uploading parties')
        )

        party = 0

        # reset progress bar
        current_progress = 0
        self.set_progress_bar(current_progress)
        total_layer = len(self.data['locations']['features'])
        progress_block = 100 / total_layer

        post_url = self._url_post_parties()

        if not post_url:
            # Project is not uploaded
            return

        for layer in self.data['locations']['features']:
            if 'party_name' in layer['fields'] and \
               'party_type' in layer['fields']:
                post_data = QByteArray()
                post_data.append('name=%s&' % layer['fields']['party_name'])
                post_data.append('type=%s&' % layer['fields']['party_type'])

                connector = ApiConnect(get_url_instance() + post_url)
                status, result = self._call_post(connector, post_data)

                if status:
                    party += 1
                    try:
                        result_dict = json.loads(result)
                        if 'id' in result_dict:
                            layer['party_id'] = result_dict['id']
                    except ValueError as e:
                        LOGGER.exception('message')
                else:
                    self.set_progress_bar(0)
                    self.set_status(
                        tr('Error: ') + result
                    )
            else:
                self.set_status(
                    tr('No party attributes found')
                )
            current_progress += progress_block
            self.set_progress_bar(current_progress)

        if party == 0:
            self.set_status(
                tr('Not uploading any party')
            )
        else:
            self.set_status(
                tr('Finished uploading {party} party'.format(party=party))
            )

        self.set_progress_bar(100)

    def upload_relationships(self):
        """Upload relationships attribute to cadasta."""
        self.set_status(
            tr('Uploading relationship')
        )

        # reset progress bar
        current_progress = 0
        self.set_progress_bar(current_progress)
        total_layer = len(self.data['locations']['features'])
        progress_block = 100 / total_layer

        relationship = 0

        url = self._url_post_relationships()

        for layer in self.data['locations']['features']:

            if 'relationship_type' in layer['fields'] and \
                    'spatial_id' in layer and \
                    'party_id' in layer:

                post_data = QByteArray()
                post_data.append('tenure_type=%s&' % (
                    layer['fields']['relationship_type']
                ))
                post_data.append('spatial_unit=%s&' % layer['spatial_id'])
                post_data.append('party=%s&' % layer['party_id'])

                connector = ApiConnect(get_url_instance() + url)
                status, result = self._call_post(connector, post_data)

                if status:
                    relationship += 1
                else:
                    self.set_progress_bar(0)
                    self.set_status(
                        tr('Error: ') + result
                    )
            else:
                self.set_status(
                    tr('No relationship attributes found')
                )

            current_progress += progress_block
            self.set_progress_bar(current_progress)

        if relationship == 0:
            self.set_status(
                tr('Not uploading any relationship')
            )
        else:
            self.set_status(
                tr('Finished uploading {num} relationship'.format(
                    num=relationship
                ))
            )

        self.set_progress_bar(100)

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return None

    def _call_post(self, connector, post_data):
        """Call post method from connector.

        For testing purpose.

        :param connector: Api connector instance
        :type connector: ApiConnect

        :param post_data: data to post
        :type post_data: QByteArray

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        return connector.post(post_data)

    def _call_json_post(self, connector, post_data):
        """Call post method with json string from connector.

        For testing purpose.

        :param connector: Api connector instance
        :type connector: ApiConnect

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        return connector.post_json(post_data)
