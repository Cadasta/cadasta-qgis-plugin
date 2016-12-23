# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 2 : Attribute Selection

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)


class StepProjectCreation2(WizardStep, FORM_CLASS):
    """Step 2 for project creation"""

    def __init__(self, parent=None):
        """Constructor

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectCreation2, self).__init__(parent)
        self.layer = None
        self.layer_attributes = None

    def attributes(self):
        """Returns data from the layer

        :returns: attributes layer selected
        :rtype: list of dict or none
        """
        cadasta_field = {
            'location_attribute': self.location_attribute_box.currentText(),
            'location_type': self.location_type_box.currentText(),
            'party_name': self.party_name_box.currentText(),
            'party_type': self.party_type_box.currentText(),
            'party_attribute': self.party_attribute_box.currentText(),
            'relationship_type': self.relationship_type_box.currentText(),
            'relationship_attribute':
                self.relationship_attribute_box.currentText(),

        }

        cadasta_data = []

        for layer in self.layer_attributes:
            for key, value in cadasta_field.iteritems():
                if value in layer:
                    cadasta_data.append(
                        {key: layer[value] if layer[value] else ''}
                    )

        return cadasta_data

    def set_widgets(self):
        """Set all widgets on the tab."""
        field_names = [field.name() for field in self.layer.pendingFields()]

        self.layer_attributes = []

        for elem in self.layer.getFeatures():
            self.layer_attributes.append(
                (dict(zip(field_names, elem.attributes())))
            )

        if 'id' in field_names:
            field_names.remove(u'id')

        field_names.insert(0, ' ')

        self.location_attribute_box.addItems(field_names)
        self.location_type_box.addItems(field_names)
        self.party_name_box.addItems(field_names)
        self.relationship_type_box.addItems(field_names)
        self.party_type_box.addItems(field_names)
        self.party_attribute_box.addItems(field_names)
        self.relationship_attribute_box.addItems(field_names)

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
        new_step = self.parent.step_project_creation03
        return new_step
