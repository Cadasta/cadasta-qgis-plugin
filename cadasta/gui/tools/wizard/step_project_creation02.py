# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 2 : Attribute Selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from qgis.gui import QgsMessageBar
from cadasta.gui.tools.utilities.edit_text_dialog import EditTextDialog
from cadasta.gui.tools.utilities.questionnaire import QuestionnaireUtility
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)


class StepProjectCreation2(WizardStep, FORM_CLASS, QuestionnaireUtility):
    """Step 2 for project creation."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectCreation2, self).__init__(parent)
        self.layer = None
        self.layer_attributes = None
        self.questionnaire = None

    def cadasta_fields(self):
        """Returns layer fields that mapped to cadasta attribute.

        :returns: cadasta fields
        :rtype: dict
        """
        cadasta_fields = {
            'location_type': self.location_type_box.currentText(),
            'party_name': self.party_name_box.currentText(),
            'party_type': self.party_type_box.currentText(),
            'relationship_type': self.relationship_type_box.currentText(),
        }

        return cadasta_fields

    def cadasta_fields_reversed(self):
        """Returns cadasta attribute that mapped to layer fields.

        :returns: cadasta fields
        :rtype: dict
        """
        cadasta_mapped_fields = {
            self.location_type_box.currentText(): 'location_type',
            self.party_name_box.currentText(): 'party_name',
            self.party_type_box.currentText(): 'party_type',
            self.relationship_type_box.currentText(): 'relationship_type',
        }

        return cadasta_mapped_fields

    def set_widgets(self):
        """Set all widgets on the tab."""
        if not self.layer or self.layer != self.parent.layer:
            self.layer = self.parent.layer
            self.set_attributes_box()
        self.questionnaire_button.clicked.connect(
            self.show_questionnaire
        )
        self.check_questionnaire()

    def set_items_combo_box(self, combo_box, field_names):
        """Set items for combo box.

        :param combo_box: combo box that will be filled.
        :type combo_box: QComboBox

        :param field_names: fields that will be filled to combo box.
        :type field_names: [str]

        """
        field_names.sort()
        combo_box.clear()
        combo_box.addItems(field_names)

        # set combo box listener for update questionnaire
        combo_box.currentIndexChanged.connect(
            self.check_questionnaire
        )

    def set_attributes_box(self):
        """Set all attribute box widgets."""
        field_names = [field.name() for field in self.layer.pendingFields()]

        self.layer_attributes = []

        for elem in self.layer.getFeatures():
            self.layer_attributes.append(
                (dict(zip(field_names, elem.attributes())))
            )

        field_names.append('--------- {field} ----------'.format(
                field=tr('No field')))
        self.set_items_combo_box(self.location_type_box, field_names)
        self.set_items_combo_box(self.party_name_box, field_names)
        self.set_items_combo_box(self.relationship_type_box, field_names)
        self.set_items_combo_box(self.party_type_box, field_names)

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        error_message = ''
        if not self.location_type_box.currentText() or \
                    tr('No field') in self.location_type_box.currentText():
            error_message = tr(
                'Empty location type. '
            )

        return (
            error_message == '',
            error_message
        )

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        new_step = self.parent.step_project_creation03
        return new_step

    def check_questionnaire(self):
        """Method when questionnaire check button is changed.
        """
        self.questionnaire = self.generate_new_questionnaire(
            self.layer, self.cadasta_fields_reversed(), '',
        )

    def show_questionnaire(self):
        """Method to show current questionnaire.
        """
        self.input_dialog = EditTextDialog(
            self, self.parent.iface, self.questionnaire)
        self.input_dialog.edit_text_done.connect(self.edit_text_dialog_done)

    def edit_text_dialog_done(self):
        """Method when edit text dialog is done.
        """
        self.questionnaire = self.input_dialog.get_text()
