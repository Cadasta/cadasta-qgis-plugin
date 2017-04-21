# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 3 : Upload to cadasta

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import os
import json
import logging
from qgis.core import (
    QgsVectorLayer,
    QgsMapLayerRegistry,
    QgsField,
    QGis,
    QgsFeature,
    QCoreApplication
)
from PyQt4.QtCore import QByteArray, QVariant
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.utilities.i18n import tr
from cadasta.utilities.utilities import Utilities
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.common.setting import get_url_instance
from cadasta.api.api_connect import ApiConnect
from cadasta.api.organization_project import (
    OrganizationProjectSpatial
)
from cadasta.common.setting import get_csv_path
from cadasta.vector import tools

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation3(WizardStep, FORM_CLASS):
    """Step 3 for project creation."""

    upload_increment = 20

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
        self.spatial_api = None

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

        step_2_data, questionnaire = self.parent.step_2_data()
        self.set_progress_bar(self.current_progress + 25)

        self.data = step_1_data
        self.data['questionnaire'] = questionnaire

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
                    del location['properties'][layer_field]

        self.set_progress_bar(100)

        self.set_status(
            tr('Finished processing data')
        )

        # Upload project
        self.upload_project()

    def check_requirement(self):
        """Checking attributes that required.

        :return: Is missed
        :rtype: bool
        """
        requirement_miss = False
        for location in self.data['locations']['features']:
            try:
                location['fields']['location_type']
            except KeyError:
                self.set_progress_bar(0)
                self.set_status(
                    Utilities.extract_error_detail(
                        tr('Location_type is not found in attribute. '
                           'Please update before uploading again.')
                    )
                )
                requirement_miss = True
                break
        return requirement_miss

    def upload_project(self):
        """Upload project to cadasta."""
        # check requirement attributes
        if self.check_requirement():
            return

        self.set_status(
            tr('Uploading project')
        )
        self.current_progress = 0
        self.set_progress_bar(self.current_progress)

        post_data = {
            'name': self.data['project_name'],
            'description': self.data['description'],
            'extent': self.data['extent'],
            'access': 'private' if self.data['private'] else 'public',
            'contacts': self.data['contacts']
        }

        if self.data['project_url']:
            post_data['urls'] = [
                self.data['project_url']
            ]

        post_url = '/api/v1/organizations/%s/projects/' % (
            self.data['organisation']['slug']
        )

        post_data = json.dumps(post_data)
        connector = ApiConnect(get_url_instance() + post_url)
        status, result = self._call_json_post(
            connector,
            post_data)

        self.set_progress_bar(self.current_progress + self.upload_increment)
        self.set_status(
            tr('Finished uploading project')
        )

        if status:
            self.project_upload_result = result
            upload_questionnaire_attribute = False
            # create questionnaire first
            # after creating location, questionnaire is blocked
            if self.data['questionnaire']:
                upload_questionnaire_attribute = True
                self.update_questionnaire_project()
            total_locations = len(self.data['locations']['features'])
            if total_locations > 0:
                self.upload_locations(upload_questionnaire_attribute)
                self.upload_parties()
                self.upload_relationships()
            self.rerender_saved_layer()
            self.set_progress_bar(100)
        else:
            self.set_progress_bar(0)
            self.set_status(
                Utilities.extract_error_detail(result)
            )

        self.set_status(tr('Finished'))

    def rerender_saved_layer(self):
        """Rerender saved layer on cadasta."""
        # rerender current project to cadasta data
        layer = self.parent.layer
        self.spatial_api = OrganizationProjectSpatial(
            self.data['organisation']['slug'],
            self.project_upload_result['slug'],
            on_finished=self.organization_projects_spatial_call_finished)

    def organization_projects_spatial_call_finished(self, result):
        """Function when Organization Project Spatial Api finished.

        :param result: result of request
        :type result: (bool, list/dict/str)
        """
        if result[0]:
            # save result to local file
            organization_slug = result[2]
            project_slug = result[3]
            vlayers = Utilities.save_layer(
                result[1], organization_slug, project_slug)
            relationship_layer = self.relationships_layer(
                vlayers,
                organization_slug,
                project_slug)
            party_layer = self.parties_layer(
                organization_slug,
                project_slug
            )
            QCoreApplication.processEvents()
            Utilities.save_project_basic_information(
                information=self.project_upload_result,
                vlayers=vlayers,
                relationship_layer_id=relationship_layer.id(),
                party_layer_id=party_layer.id()
            )
        else:
            pass

    def upload_locations(self, update_questionnaire_attribute):
        """Upload project locations to cadasta.

        :param update_questionnaire_attribute: Boolean to check if it need to
         upload the attributes
        :type update_questionnaire_attribute: bool
        """
        self.set_status(
            tr('Uploading locations')
        )
        total_locations = len(self.data['locations']['features'])
        progress_left = \
            (100 - self.current_progress - self.upload_increment) \
            / total_locations

        post_url = '/api/v1/organizations/%s/projects/%s/spatial/' % (
            self.data['organisation']['slug'],
            self.project_upload_result['slug']
        )

        failed = 0

        for location in self.data['locations']['features']:
            post_data = {
                'geometry': location['geometry'],
                'type': location['fields']['location_type']
            }

            if update_questionnaire_attribute:
                if location['properties']:
                    post_data['attributes'] = location['properties']
                if 'id' in post_data['attributes']:
                    del post_data['attributes']['id']

            connector = ApiConnect(get_url_instance() + post_url)
            status, result = self._call_json_post(
                connector,
                json.dumps(post_data))

            if status:
                self.set_progress_bar(self.current_progress + progress_left)
                try:
                    result_obj = result
                    if 'properties' in result_obj:
                        location['spatial_id'] = result_obj['properties'][
                            'id']
                except ValueError as e:
                    LOGGER.exception('message')
            else:
                self.set_progress_bar(0)
                self.set_status(
                    Utilities.extract_error_detail(result)
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
                        result_dict = result
                        if 'id' in result_dict:
                            layer['party_id'] = result_dict['id']
                    except ValueError as e:
                        LOGGER.exception('message')
                else:
                    self.set_progress_bar(0)
                    self.set_status(
                        Utilities.extract_error_detail(result)
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
                        Utilities.extract_error_detail(result)
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

    def update_questionnaire_project(self):
        """Update questionnaire."""
        self.set_status(
            tr('Update questionnaire')
        )
        post_url = '/api/v1/organizations/' \
                   '%s/projects/%s/questionnaire/' % (
                       self.data['organisation']['slug'],
                       self.project_upload_result['slug']
                   )

        post_data = QByteArray()
        post_data.append(self.data['questionnaire'])

        connector = ApiConnect(get_url_instance() + post_url)
        status, result = self._call_json_put(connector, post_data)

        self.set_status(
            tr('Finished update questionnaire')
        )
        if status:
            self.set_progress_bar(
                self.current_progress + self.upload_increment)
        else:
            self.set_progress_bar(0)
            self.set_status(
                Utilities.extract_error_detail(result)
            )

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

    def _call_json_put(self, connector, post_data):
        """Call put method with json string from connector.

        For testing purpose.

        :param connector: Api connector instance
        :type connector: ApiConnect

        :param post_data: data to post
        :type post_data: str

        :returns: Tuple of post status and results
        :rtype: ( bool, str )
        """
        return connector.put_json(post_data)

    def relationships_layer(
            self, vector_layers, organization_slug, project_slug):
        """Create relationship layer.

        :param vector_layers: List of QGS vector layer in memory
        :type vector_layers: list of QgsVectorLayer

        :param organization_slug: Organization slug
        :type organization_slug: str

        :param project_slug: Project slug
        :type project_slug: str

        :return: Relationship layer
        :rtype: QgsVectorLayer
        """
        attribute = 'relationships'

        api = '/api/v1/organizations/{organization_slug}/projects/' \
              '{project_slug}/spatial/{spatial_unit_id}/relationships/'

        csv_path = get_csv_path(
            organization_slug,
            project_slug,
            attribute)

        if os.path.isfile(csv_path):
            os.remove(csv_path)

        relationship_layer = tools.create_memory_layer(
            layer_name='%s/%s/%s' % (
                organization_slug,
                project_slug,
                attribute),
            geometry=QGis.NoGeometry,
            fields=[
                QgsField('spatial_id', QVariant.String, "string"),
                QgsField('rel_id', QVariant.String, "string"),
                QgsField('rel_name', QVariant.String, "string"),
                QgsField('party_id', QVariant.String, "string"),
            ]
        )

        QgsMapLayerRegistry.instance().addMapLayer(relationship_layer)

        for vector_layer in vector_layers:
            # Add relationship layer id to spatial attribute table
            spatial_id_index = vector_layer.fieldNameIndex('id')

            for index, feature in enumerate(vector_layer.getFeatures()):
                attributes = feature.attributes()
                spatial_api = api.format(
                    organization_slug=organization_slug,
                    project_slug=project_slug,
                    spatial_unit_id=attributes[spatial_id_index]
                )
                connector = ApiConnect(get_url_instance() + spatial_api)
                status, results = connector.get()

                if not status or len(results) == 0:
                    continue

                try:
                    for result in results:
                        relationship_layer.startEditing()
                        fet = QgsFeature()
                        questionnaire_attr = result['attributes']
                        if not questionnaire_attr:
                            questionnaire_attr = '-'
                        fet.setAttributes([
                            attributes[spatial_id_index],
                            result['id'],
                            result['tenure_type'],
                            result['party']['id'],
                        ])
                        relationship_layer.addFeature(fet, True)
                        relationship_layer.commitChanges()
                except (IndexError, KeyError):
                    continue

        Utilities.add_tabular_layer(
            relationship_layer,
            organization_slug,
            project_slug,
            attribute
        )

        return relationship_layer

    def parties_layer(self, organization_slug, project_slug):
        """Create parties layer.

        :param organization_slug: Organization slug
        :type organization_slug: str

        :param project_slug: Project slug
        :type project_slug: str

        :param vector_layer: QGS vector layer in memory
        :type vector_layer: QgsVectorLayer
        """
        attribute = 'parties'

        csv_path = get_csv_path(organization_slug, project_slug, attribute)

        if os.path.isfile(csv_path):
            os.remove(csv_path)

        api = '/api/v1/organizations/{organization_slug}/projects/' \
              '{project_slug}/parties/'.format(
            organization_slug=organization_slug,
            project_slug=project_slug)

        connector = ApiConnect(get_url_instance() + api)
        status, results = connector.get()

        if not status:
            return

        party_layer = tools.create_memory_layer(
            layer_name='%s/%s/%s' % (
                organization_slug,
                project_slug,
                attribute),
            geometry=QGis.NoGeometry,
            fields=[
                QgsField('id', QVariant.String, "string"),
                QgsField('name', QVariant.String, "string"),
                QgsField('type', QVariant.String, "string"),
            ]
        )

        QgsMapLayerRegistry.instance().addMapLayer(party_layer)

        for party in results:
            party_layer.startEditing()
            feature = QgsFeature()
            questionnaire_attr = party['attributes']
            if not questionnaire_attr:
                questionnaire_attr = '-'
            feature.setAttributes([
                party['id'],
                party['name'],
                party['type'],
            ])
            party_layer.addFeature(feature, True)
            party_layer.commitChanges()
            QCoreApplication.processEvents()

        Utilities.add_tabular_layer(
            party_layer,
            organization_slug,
            project_slug,
            attribute
        )

        return party_layer
