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
    QMovie,
    QCursor
)
from PyQt4.QtCore import Qt
from operator import itemgetter
from cadasta.api.project import Project
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import resources_path
from cadasta.utilities.utilities import Utilities
from cadasta.model.contact import Contact
from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.gui.tools.widget.contact_widget import ContactWidget
from cadasta.common.setting import (
    set_setting,
    get_setting
)

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectDownload01(WizardStep, FORM_CLASS):
    """Step 1 for project download."""

    def __init__(self, iface=None, parent=None):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectDownload01, self).__init__(parent)
        self.iface = iface
        self.project_api = None
        self.current_contacts = None
        self.add_contact_enabled = False

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project_combo_box.currentIndexChanged.connect(
            self.project_combo_box_changed)

        checkbox_checked = get_setting('public_project')
        if checkbox_checked:
            self.public_projects_checkbox.setCheckState(
                Qt.Checked
            )
        self.public_projects_checkbox.stateChanged.connect(
            self.public_check_box_changed)

        icon_path = resources_path('images', 'throbber.gif')
        movie = QMovie(icon_path)
        self.throbber_loader.setMovie(movie)
        movie.start()
        self.get_available_projects()
        self.add_contact_label.mousePressEvent = self.add_contact_label_clicked
        self.set_enabled_add_contact_label(False)

    def add_contact_label_clicked(self, event):
        """Handler for add_contact_label clicked. """
        if self.add_contact_enabled:
            self.add_to_contacts()

    def set_enabled_add_contact_label(self, enabled):
        """Set add_contact_label enabled or disabled.

        :param enabled: Flag to disable or enabled label
        :type enabled: bool
        """
        self.add_contact_enabled = enabled
        if not enabled:
            self.add_contact_label.setStyleSheet('color: gray;')
            self.add_contact_label.setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.add_contact_label.setStyleSheet('color: blue;')
            self.add_contact_label.setCursor(QCursor(Qt.PointingHandCursor))

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

    def public_check_box_changed(self, state):
        """Public project check box's state changed.

        :param state: Checkbox state
        :type state: int
        """
        set_setting('public_project', state == Qt.Checked)
        if self.project_api:
            self.project_api.cancel_request()
        self.project_combo_box.clear()
        self.get_available_projects()

    def project_combo_box_changed(self):
        """Update description when combo box changed."""
        project = self.selected_project()
        if not project:
            self.project_description_label.setText(tr(
                'This is the read only project description that '
                'changes when the combo box above is changed.'
            ))
            self.project_url_label.setText('-')
            self.contact_information_label.setText('-')
            self.privacy_status_label.setText('-')
            self.set_enabled_add_contact_label(False)
            return

        if project['description']:
            self.project_description_label.setText(
                    self.tr(project['description'].encode('utf-8')))
        else:
            self.project_description_label.setText(
                    self.tr(project['name'].encode('utf-8')))

        if project['urls']:
            project_urls = ''
            for url in project['urls']:
                project_urls += url + ' \n'

            if not project_urls.isspace():
                project_urls = project_urls[:-2]
                self.project_url_label.setText(project_urls)
            else:
                self.project_url_label.setText('-')
        else:
            self.project_url_label.setText('-')

        if project['contacts']:
            project_contacts = ''
            for contact in project['contacts']:
                project_contacts += contact['name']
                if 'email' in contact and contact['email']:
                    project_contacts += ', ' + contact['email']
                if 'tel' in contact and contact['tel']:
                    project_contacts += ', ' + contact['tel']
                project_contacts += ' \n'

            if project_contacts:
                self.set_enabled_add_contact_label(True)
                self.current_contacts = project['contacts']
                project_contacts = project_contacts[:-2]
                self.contact_information_label.setText(project_contacts)
        else:
            self.contact_information_label.setText('-')
            self.set_enabled_add_contact_label(False)

        if project['access']:
            self.privacy_status_label.setText(project['access'].title())

    def get_available_projects(self):
        """Get available projects."""
        self.throbber_loader.setVisible(True)
        self.project_api = Project(
            on_finished=self.get_available_projects_finished)

    def add_to_contacts(self):
        """Open contacts dialog and add current selected contacts to db."""
        if not self.current_contacts:
            return

        for contact in self.current_contacts:
            contact_from_db = Contact.get_rows(
                name=contact['name'],
                phone=contact['tel'],
                email=contact['email']
            )
            if not contact_from_db:
                new_contact = Contact()
                new_contact.name = contact['name']
                new_contact.email = contact['email']
                new_contact.phone = contact['tel']
                new_contact.save()

        # Open contact dialog
        dialog = CadastaDialog(
            iface=self.iface,
            subtitle='Contact',
            widget=ContactWidget()
        )
        dialog.show()
        dialog.exec_()
