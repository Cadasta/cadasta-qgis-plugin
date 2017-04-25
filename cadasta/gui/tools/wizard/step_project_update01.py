# coding=utf-8
"""
Cadasta project update step -**Cadasta Wizard**

This module provides: Project Update Step 1 : Organisation selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from PyQt4.QtGui import (
    QMovie
)
from PyQt4.QtCore import QCoreApplication
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.utilities.resources import resources_path
from cadasta.utilities.utilities import Utilities
from cadasta.api.organization import Organization
from cadasta.api.organization_project import OrganizationList

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate01(WizardStep, FORM_CLASS):
    """Step 1 for project update."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate01, self).__init__(parent)
        self.parent = parent
        self.project_api = None
        self.organization = None

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
        new_step = self.parent.step_project_update02
        return new_step

    def get_available_projects_finished(self, projects):
        """Function when Project Api finished.

        :param projects: list downloaded projects
        :type projects: list of dict
        """
        self.project_combo_box.clear()

        if not projects:
            return

        projects = sorted(projects, key=lambda k: k['name'])

        unique_projects = []
        for project in projects:
            project_descriptions = project['name'].split('/')
            organization = project_descriptions[0]
            name = project_descriptions[1]
            layer_name = '%s/%s' % (organization, name)
            if layer_name not in unique_projects:
                unique_projects.append(layer_name)
                self.project_combo_box.addItem(
                    layer_name, project
                )

        self.throbber_loader.setVisible(False)

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
                    self.tr('No description'))

            if project['information']['urls']:
                project_urls = ''
                for url in project['information']['urls']:
                    project_urls += url + ' \n'

                if not project_urls.isspace():
                    project_urls = project_urls[:-2]
                    self.project_url_label.setText(project_urls)
                else:
                    self.project_url_label.setText('-')
            else:
                self.project_url_label.setText('-')

            if project['information']['contacts']:
                project_contacts = ''
                for contact in project['information']['contacts']:
                    project_contacts += contact['name']
                    if 'email' in contact and contact['email']:
                        project_contacts += ', ' + contact['email']
                    if 'tel' in contact and contact['tel']:
                        project_contacts += ', ' + contact['tel']
                    project_contacts += ' \n'

                if project_contacts:
                    project_contacts = project_contacts[:-2]
                    self.contact_information_label.setText(project_contacts)
            else:
                self.contact_information_label.setText('-')

            if project['information']['access']:
                self.privacy_status_label.setText(
                        project['information']['access'].title())

        except (TypeError, KeyError):
            self.project_description_label.setText(
                self.tr('No description'))
            self.project_url_label.setText('-')
            self.contact_information_label.setText('-')
            self.privacy_status_label.setText('-')
            return

    def get_downloaded_project(self, results):
        """Get downloaded project from organization slug.

        :param results: result of request
        :type results: (bool, list/dict/str)
        """
        projects = []
        if not results[0]:
            self.throbber_loader.setVisible(False)
            return

        for organization in results[1]:
            projects.extend(
                Utilities.get_downloaded_projects(organization['slug'])
            )
        self.get_available_projects_finished(projects)

    def get_available_projects(self):
        """Get available projects."""
        self.throbber_loader.setVisible(True)
        self.organization = OrganizationList(
            permissions='project.create',
            on_finished=self.get_downloaded_project
        )
