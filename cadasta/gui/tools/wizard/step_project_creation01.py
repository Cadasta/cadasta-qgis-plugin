# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 1 : Organisation and layer selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from qgis.PyQt.QtCore import pyqtSignature
from cadasta.utilities.resources import is_valid_url
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.api.organization import Organization

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation1(WizardStep, FORM_CLASS):
    """Step 1 for project creation"""

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.btnGetOrganisation.clicked.connect(
                self.get_available_organisations
        )
        self.get_available_layers()

    def project_name(self):
        """Get project name from input.

        :returns: Project name
        :rtype: str
        """
        return self.inputProjectName.displayText()

    def project_url(self):
        """Get project url from input.

        :returns: Project url
        :rtype: str
        """
        return self.inputProjectUrl.displayText()

    def selected_layer(self):
        """Get selected layer from combo box.

        :returns: Layer data
        :rtype: object
        """
        layer_data = self.cbxQgisLayer.itemData(
                self.cbxQgisLayer.currentIndex()
        )
        return layer_data

    def selected_organisation(self):
        """Get selected organisation from combo box.

        :returns: Organisation data
        :rtype: dict
        """
        organisation_data = self.cbxOrganisation.itemData(
                self.cbxOrganisation.currentIndex()
        )
        return organisation_data

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        error_message = ''

        if not self.project_url() or \
                not is_valid_url(self.project_url()):
            error_message += tr(
                'Missing or Invalid url. \n'
            )

        if not self.project_name():
            error_message += tr(
                'Empty project name. '
            )

        if not self.selected_organisation():
            error_message += tr(
                'Empty Organisation. '
            )

        return (
            error_message is None,
            error_message
        )

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        new_step = self.parent.step_project_creation02
        return new_step

    def get_available_organisations(self):
        """Get available organisations."""
        LOGGER.info('Getting organisations')
        organization = Organization()
        status, results = organization.all_organizations()
        if status:
            self.cbxOrganisation.clear()
            self.parent.organisations_list = results
            for organisation in results:
                self.cbxOrganisation.addItem(
                    organisation['name'],
                    organisation
                )
        else:
            self.message_bar.pushWarning(
                    self.tr('Error'),
                    self.tr(results)
            )

    def get_available_layers(self):
        """Get layer from qgis and load it to combo box."""
        layers = self.parent.iface.legendInterface().layers()
        for layer in layers:
            self.cbxQgisLayer.addItem(
                    layer.name(),
                    layer
            )
