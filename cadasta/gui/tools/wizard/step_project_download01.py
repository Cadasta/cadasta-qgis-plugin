# coding=utf-8
"""
Cadasta project download step -**Cadasta Wizard**

This module provides: Project Download Step 1 : Project selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from PyQt4.QtGui import (
    QMovie
)
from operator import itemgetter
from cadasta.api.project import Project
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import resources_path
from cadasta.utilities.utilities import Utilities

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectDownload01(WizardStep, FORM_CLASS):
    """Step 1 for project download."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectDownload01, self).__init__(parent)
        self.project_api = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project_combo_box.currentIndexChanged.connect(
            self.project_combo_box_changed)
        icon_path = resources_path('images', 'throbber.gif')
        movie = QMovie(icon_path)
        self.throbber_loader.setMovie(movie)
        movie.start()
        self.get_available_projects()

    def selected_project(self):
        """Get selected project from combo box.

        :returns: Project data
        :rtype: dict
        """
        project_data = self.project_combo_box.itemData(
            self.project_combo_box.currentIndex()
        )
        return project_data

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        error_message = ''

        if not self.selected_project():
            error_message += tr(
                'Missing project.'
            )

        return (
            error_message == '',
            error_message
        )

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        new_step = self.parent.step_project_download02
        return new_step

    def get_available_projects_finished(self, result):
        """Function when Project Api finished.

        :param result: result of request
        :type result: (bool, list/dict/str)
        """
        self.throbber_loader.setVisible(False)
        self.project_combo_box.clear()
        if result[0]:
            projects = sorted(result[1], key=itemgetter('slug'))

            processed_downloaded_projects = []
            downloaded_projects = Utilities.get_all_downloaded_projects()

            for downloaded_project in downloaded_projects:
                project_descriptions = downloaded_project['name'].split('/')
                organization = project_descriptions[0]
                name = project_descriptions[1]
                processed_downloaded_projects.append(
                    (organization + '-' + name).encode('utf-8')
                )

            for index, project in enumerate(projects):

                project_slug = '{organization_slug}-{project_slug}'.format(
                    organization_slug=project['organization']['slug'].encode(
                            'utf-8'),
                    project_slug=project['slug'].encode('utf-8'))

                self.project_combo_box.addItem(
                    project['name'], project)
                self.project_combo_box.setCurrentIndex(index)

                self.project_combo_box.model().item(index).setEnabled(
                    project_slug not in processed_downloaded_projects
                )

            # Set selected to first item
            self.project_combo_box.setCurrentIndex(0)

        else:
            pass

    def project_combo_box_changed(self):
        """Update description when combo box changed."""
        project = self.selected_project()
        if project['description']:
            self.project_description_label.setText(
                    self.tr(project['description'].encode('utf-8')))
        else:
            self.project_description_label.setText(
                    self.tr(project['name'].encode('utf-8')))

    def get_available_projects(self):
        """Get available projects."""
        self.throbber_loader.setVisible(True)
        self.project_api = Project(
            on_finished=self.get_available_projects_finished)
