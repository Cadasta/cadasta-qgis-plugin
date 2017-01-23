# coding=utf-8
"""
Cadasta project update step -**Cadasta Wizard**

This module provides: Project Update Step 3 : Download project spatial data

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import json
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsField
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.common.setting import get_url_instance
from cadasta.common.setting import get_path_data
from cadasta.api.organization_project import (
    OrganizationProjectSpatial
)
from cadasta.api.api_connect import ApiConnect

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
        self.parent = parent
        self.project = None
        self.loading_label_string = None
        self.loaded_label_string = None
        self.spatial_api = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project = self.parent.project
        self.loading_label_string = self.tr('Your data is being downloaded')
        self.loaded_label_string = self.tr('Your data has been downloaded')

        self.warning_label.setText(self.loading_label_string)
        self.get_project_spatial(
                self.project['organization']['slug'], self.project['slug'])
        self.parent.next_button.setEnabled(False)

    def get_project_spatial(self, organization_slug, project_slug):
        """Call Organization Project Spatial api.

        :param project_slug: project_slug for getting spatial
        :type project_slug: str
        """
        self.spatial_api = OrganizationProjectSpatial(
            organization_slug,
            project_slug,
            on_finished=self.organization_projects_spatial_call_finished)

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return self.parent.step_project_update04

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

    def get_relationship_attribute(self, vector_layer):
        """Get parties listed as part of a project and put it to attribute table.

        :param vector_layer: QGS vector layer in memory
        :type vector_layer: QgsVectorLayer
        """
        organization_slug = self.project['organization']['slug']
        project_slug = self.project['slug']

        api = '/api/v1/organizations/{organization_slug}/projects/' \
              '{project_slug}/parties/'.format(
                organization_slug=organization_slug,
                project_slug=project_slug)

        connector = ApiConnect(get_url_instance() + api)
        status, result = connector.get()

        if not status or len(result) == 0:
            return

        self.parent.parties = result

        # Add party attribute to location
        data_provider = vector_layer.dataProvider()

        # Enter editing mode
        vector_layer.startEditing()

        # Add fields
        data_provider.addAttributes([
            QgsField('party_id', QVariant.String),
            QgsField('party_name', QVariant.String),
            QgsField('party_type', QVariant.String),
        ])

        # Save the new fields
        vector_layer.commitChanges()

        # Edit the attribute value
        vector_layer.startEditing()

        # Features
        features = vector_layer.getFeatures()
        for index, fet in enumerate(features):
            try:
                vector_layer.changeAttributeValue(
                    fet.id(), 3, result[index]['id']
                )
                vector_layer.changeAttributeValue(
                    fet.id(), 4, result[index]['name']
                )
                vector_layer.changeAttributeValue(
                    fet.id(), 5, result[index]['type']
                )
            except (IndexError, KeyError):
                pass

        # Commit changes
        vector_layer.commitChanges()

    def save_layer(self, geojson, organization_slug, project_slug):
        """Save geojson to local file.

        :param organization_slug: organization slug for data
        :type organization_slug: str

        :param project_slug: project_slug for getting spatial
        :type project_slug: str

        :param geojson: geojson that will be saved
        :type geojson: JSON object
        """
        filename = get_path_data(organization_slug, project_slug)
        file_ = open(filename, 'w')
        file_.write(json.dumps(geojson, sort_keys=True))
        file_.close()
        vlayer = QgsVectorLayer(
            filename, "%s/%s" % (organization_slug, project_slug), "ogr")
        self.get_relationship_attribute(vlayer)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        self.parent.layer = vlayer
        self.parent.locations = geojson
