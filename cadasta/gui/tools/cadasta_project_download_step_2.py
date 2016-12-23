# -*- coding: utf-8 -*-
"""Contains project download step 2 dialog.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

import json
import logging

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar
from cadasta.api.organization_project import (
    OrganizationProject,
    OrganizationProjectSpatial
)
from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.utilities.resources import get_ui_class
from cadasta.common.setting import get_path_data

FORM_CLASS = get_ui_class('cadasta_project_download_step_2.ui')
LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaProjectDownloadStep2(CadastaDialog, FORM_CLASS):
    """Dialog class for downloading data.

    This class will download all layer based on organization
    that is selected from organization_slug
    """

    def __init__(self, organization_slug, step_1_dialog=None, parent=None):
        """Constructor.

        :param organization_slug: organization slug for data
        :type organization_slug: str
        """

        super(CadastaProjectDownloadStep2, self).__init__(parent)
        self.step_1_dialog = step_1_dialog
        self.setupUi(self)
        self.message_bar = None
        self.projects = None
        self.init_style()
        self.spatial_api = []
        self.close_button.clicked.connect(self.close_dialog)
        self.step_1_button.clicked.connect(self.goto_step_1)

        # download project
        self.organization_slug = organization_slug
        self.get_projects()

    def init_style(self):
        """Initiate custom style for widgets. """

        self.enable_button(self.step_1_button)
        self.disable_button(self.step_2_button)
        self.disable_button(self.close_button)

    def goto_step_1(self):
        """Go to step 1 dialog"""

        if self.step_1_dialog:
            self.close()
            self.step_1_dialog.show()

    def close_dialog(self):
        """Close this dialog function."""
        self.close()

    def increase_progress_bar(self):
        """Increasing progress bar."""

        self.progress_bar.setValue(
            self.progress_bar.value() + self.grid_value)
        progress_bar_max = self.progress_bar.maximum()
        progress_bar_value = self.progress_bar.value()
        if progress_bar_max - progress_bar_value < self.grid_value:
            self.progress_bar.setValue(self.progress_bar.maximum())

    def get_projects(self):
        """Get project of organization list through api. """

        self.api = OrganizationProject(
            self.organization_slug,
            on_finished=self.organization_projects_call_finished)

    def organization_projects_call_finished(self, result):
        """Function when Organization Project Api finished

        :param result: result of request
        :type result: (bool, list/dict/str)
        """
        self.projects = []
        # call api done
        if result[0]:
            self.projects = result[1]
            # get grid value
            self.grid_value = self.progress_bar.maximum() / (
            len(self.projects) + 1)

            # render geojson
            for project in self.projects:
                self.get_project_spatial(project['slug'])
        else:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('Failed getting data')
            )
        self.increase_progress_bar()

    def get_project_spatial(self, project_slug):
        """Call Organization Project Spatial api.

        :param project_slug: project_slug for getting spatial
        :type project_slug: str
        """
        self.spatial_api.append(
            OrganizationProjectSpatial(
                self.organization_slug,
                project_slug,
                on_finished=self.organization_projects_spatial_call_finished)
        )

    def organization_projects_spatial_call_finished(self, result):
        """Function when Organization Project Spatial Api finished.

        :param result: result of request
        :type result: (bool, list/dict/str)
        """
        self.increase_progress_bar()
        if result[0]:
            # save result to local file
            organization_slug = result[2]
            project_slug = result[3]
            self.save_layer(result[1], organization_slug, project_slug)
        else:
            pass

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
        self.downloading_done()

    def downloading_done(self):
        """Call this when downloading data is done."""
        if self.progress_bar.value() >= 100:
            self.enable_button(self.close_button)
