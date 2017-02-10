# coding=utf-8
"""
Cadasta project download step -**Cadasta Wizard**

This module provides: Project Download Step 1 : Available project selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.api.project import Project
from cadasta.utilities.utilities import Utilities
from cadasta.api.organization import Organization

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate01(WizardStep, FORM_CLASS):
    """Step 1 for project download."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate01, self).__init__(parent)
        self.parent = parent
        self.project_api = None
        self.organization = Organization()

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.get_available_projects_button.clicked.connect(
            self.get_available_projects
        )
        self.project_combo_box.currentIndexChanged.connect(
            self.project_combo_box_changed)

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
        new_step = self.parent.step_project_update02
        return new_step

    def get_available_projects_finished(self, projects):
        """Function when Project Api finished.

        :param projects: list downloaded projects
        :type projects: list of dict
        """
        self.get_available_projects_button.setEnabled(True)
        self.project_combo_box.clear()

        if not projects:
            return

        projects = sorted(projects, key=lambda k: k['name'])
        for project in projects:
            self.project_combo_box.addItem(
                project['name'], project)

    def project_combo_box_changed(self):
        """Update description when combo box changed."""
        project = self.selected_project()
        if not project:
            return
        try:
            if project['information']['description']:
                self.project_description_label.setText(
                    self.tr(project['information']['description']))
            else:
                self.project_description_label.setText(
                    self.tr(project['name']))
        except (TypeError, KeyError):
            return

    def get_downloaded_project(self, organization_slug):
        """Get downloaded project from organization slug.

        :param organization_slug: Organization slug of project
        :type organization_slug: str
        """
        return Utilities.get_downloaded_projects(organization_slug)

    def get_available_projects(self):
        """Get available projects."""
        self.get_available_projects_button.setEnabled(False)

        # Get organization with read/update permission
        status, results = self.organization.organizations_project_filtered()

        projects = []

        if not status:
            self.get_available_projects_button.setEnabled(True)
            LOGGER.error(results)
            return

        for organization in results:
            projects.extend(
                self.get_downloaded_project(organization['slug'])
            )

        self.get_available_projects_finished(projects)
