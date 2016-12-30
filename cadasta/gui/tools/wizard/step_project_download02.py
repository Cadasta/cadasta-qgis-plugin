# coding=utf-8
"""
Cadasta project download step -**Cadasta Wizard**

This module provides: Project Download Step 2 : Download Layer

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import json
import logging
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from cadasta.common.setting import get_path_data
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.api.organization_project import (
    OrganizationProjectSpatial
)

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectDownload02(WizardStep, FORM_CLASS):
    """Step 2 for project download"""

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

    def save_layer(self, geojson, organization_slug, project_slug):
        """Save geojson to local file

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
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
