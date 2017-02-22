# coding=utf-8
"""
Cadasta project download step -**Cadasta Wizard**

This module provides: Project Download Step 2 : Download Project

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import json
import csv
import os
import logging
from uuid import uuid4
from PyQt4.QtCore import QVariant
from qgis.core import (
    QgsVectorLayer,
    QgsMapLayerRegistry,
    QgsField,
    QGis,
    QgsFeature,
    QCoreApplication)
from cadasta.common.setting import get_path_data, get_csv_path
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.utilities.geojson_parser import GeojsonParser
from cadasta.api.organization_project import (
    OrganizationProjectSpatial
)
from cadasta.utilities.utilities import Utilities
from cadasta.api.api_connect import ApiConnect
from cadasta.common.setting import get_url_instance
from cadasta.vector import tools

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectDownload02(WizardStep, FORM_CLASS):
    """Step 2 for project download."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectDownload02, self).__init__(parent)
        self.loading_label_string = None
        self.loaded_label_string = None
        self.spatial_api = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.loading_label_string = self.tr('Your data is being downloaded')
        self.loaded_label_string = self.tr('Your data have been downloaded')

        self.warning_label.setText(self.loading_label_string)
        self.get_project_spatial(
            self.project['organization']['slug'], self.project['slug'])
        self.parent.next_button.setEnabled(False)

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        return True, ''

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        return None

    def get_project_spatial(self, organization_slug, project_slug):
        """Call Organization Project Spatial api.

        :param project_slug: project_slug for getting spatial
        :type project_slug: str
        """
        self.spatial_api = OrganizationProjectSpatial(
            organization_slug,
            project_slug,
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
            self.save_layer(result[1], organization_slug, project_slug)
        else:
            pass
        self.progress_bar.setValue(self.progress_bar.maximum())
        self.parent.next_button.setEnabled(True)
        self.warning_label.setText(self.loaded_label_string)

    def parties_layer(self, vector_layer):
        """Create parties layer.

        :param vector_layer: QGS vector layer in memory
        :type vector_layer: QgsVectorLayer

        :return: Party layer
        :rtype: QgsVectorLayer
        """
        organization_slug = self.project['organization']['slug']
        project_slug = self.project['slug']
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
                layer_name='%s/%s_%s' % (
                    organization_slug,
                    project_slug,
                    attribute),
                geometry=QGis.NoGeometry,
                fields=[
                    QgsField('id', QVariant.String, "string"),
                    QgsField('name', QVariant.String, "string"),
                    QgsField('type', QVariant.String, "string"),
                    QgsField('attributes', QVariant.String, "string"),
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
                questionnaire_attr
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

    def relationships_layer(self, vector_layer):
        """Create relationship layer.

        :param vector_layer: QGS vector layer in memory
        :type vector_layer: QgsVectorLayer

        :return: Relationship layer
        :rtype: QgsVectorLayer
        """
        organization_slug = self.project['organization']['slug']
        project_slug = self.project['slug']
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
            layer_name='%s/%s_%s' % (
                organization_slug,
                project_slug,
                attribute),
            geometry=QGis.NoGeometry,
            fields=[
                QgsField('spatial_id', QVariant.String, "string"),
                QgsField('rel_id', QVariant.String, "string"),
                QgsField('rel_name', QVariant.String, "string"),
                QgsField('party_id', QVariant.String, "string"),
                QgsField('attributes', QVariant.String, "string"),
            ]
        )

        QgsMapLayerRegistry.instance().addMapLayer(relationship_layer)

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
                        questionnaire_attr,
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

    def save_layer(self, geojson, organization_slug, project_slug):
        """Save geojson to local file.

        :param organization_slug: organization slug for data
        :type organization_slug: str

        :param project_slug: project_slug for getting spatial
        :type project_slug: str

        :param geojson: geojson that will be saved
        :type geojson: JSON object
        """
        geojson = GeojsonParser(geojson)
        filename = get_path_data(organization_slug, project_slug)
        file_ = open(filename, 'w')
        file_.write(geojson.geojson_string())
        file_.close()
        vlayer = QgsVectorLayer(
            filename, "%s/%s" % (organization_slug, project_slug), "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        relationship_layer = self.relationships_layer(vlayer)
        party_layer = self.parties_layer(vlayer)
        QCoreApplication.processEvents()
        # save basic information
        Utilities.save_project_basic_information(
            self.project,
            relationship_layer.id(),
            party_layer.id()
        )
