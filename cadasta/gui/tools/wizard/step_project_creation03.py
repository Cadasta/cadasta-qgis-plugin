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
from cadasta.mixin.network_mixin import NetworkMixin
from cadasta.common.setting import get_url_instance

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation3(WizardStep, FORM_CLASS):
    """Step 3 for project creation"""

    def __init__(self, parent=None):
        """Constructor

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
                    location['fields'][cadasta_field] = properties[layer_field]
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

        network = NetworkMixin(get_url_instance() + post_url)
        network.connect_json_post(json.dumps(post_data))
        while not network.reply.isFinished():
            QCoreApplication.processEvents()

        self.set_progress_bar(self.current_progress + 25)
        self.set_status(
            tr('Finished uploading project')
        )

        if not network.error:
            self.project_upload_result = network.get_json_results()
            self.upload_locations()
            self.upload_parties()
        else:
            self.set_progress_bar(0)
            self.set_status(
                'Error: %s' % network.results.data()
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
            post_data.append('geometry=%s&' % json.dumps(location['geometry']))
            post_data.append('type=%s' % location['fields']['location_type'])

            network = NetworkMixin(get_url_instance() + post_url)
            network.connect_post(post_data)
            while not network.reply.isFinished():
                QCoreApplication.processEvents()

            if not network.error:
                self.set_progress_bar(self.current_progress + progress_left)
            else:
                self.set_progress_bar(0)
                self.set_status(
                    'Error: %s' % network.results.data()
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

        :returns: api url
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

    def _connect_post(self, network, post_data):
        """Call post method.

        :param network: Network connector
        :type network: NetworkMixin

        :param post_data: data to post
        :type post_data: QByteArray

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        network.connect_post(post_data)
        while not network.reply.isFinished():
            QCoreApplication.processEvents()

        if not network.error:
            return True, network.results.data()
        else:
            return False, network.results.data()

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

        network = NetworkMixin(get_url_instance() + post_url)

        for layer in self.data['locations']['features']:
            if layer['fields']['party_name'] and layer['fields']['party_type']:
                post_data = QByteArray()
                post_data.append('name=%s&' % layer['fields']['party_name'])
                post_data.append('type=%s&' % layer['fields']['party_type'])

                status, result = self._connect_post(network, post_data)

                if status:
                    party += 1
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
                tr('Finished uploading ') + str(party) + tr(' party')
            )

        self.set_progress_bar(100)

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        return None
