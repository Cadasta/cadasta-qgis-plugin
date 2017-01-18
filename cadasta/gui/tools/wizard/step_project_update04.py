# coding=utf-8
"""
Cadasta project update step -**Cadasta Wizard**

This module provides: Project Update Step 4 : Attribute mapping

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate04(WizardStep, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate04, self).__init__(parent)
        self.layer = None
        self.layer_attributes = None
        self.project = None

    def cadasta_fields(self):
        """Returns layer fields that mapped to cadasta attribute.

        :returns: cadasta fields
        :rtype: dict
        """
        cadasta_fields = {
            'location_attribute': self.location_attribute_box.currentField(),
            'location_type': self.location_type_box.currentField(),
            'party_name': self.party_name_box.currentField(),
            'party_type': self.party_type_box.currentField(),
            'party_attribute': self.party_attribute_box.currentField(),
            'relationship_type': self.relationship_type_box.currentField(),
            'relationship_attribute': (
                self.relationship_attribute_box.currentField()
            )
        }

        return cadasta_fields

    def set_attributes_box(self):
        """Set all attribute box widgets."""
        field_names = [field.name() for field in self.layer.pendingFields()]

        self.layer_attributes = []

        for elem in self.layer.getFeatures():
            self.layer_attributes.append(
                (dict(zip(field_names, elem.attributes())))
            )

        self.location_type_box.clear()
        self.location_type_box.setLayer(self.layer)
        self.location_type_box.setField('type')

        self.party_name_box.clear()
        self.party_name_box.setLayer(self.layer)
        self.party_name_box.setField('party_name')

        self.relationship_type_box.clear()
        self.relationship_type_box.setLayer(self.layer)
        self.relationship_type_box.setField('rel_type')

        self.party_type_box.clear()
        self.party_type_box.setLayer(self.layer)
        self.party_type_box.setField('party_type')

        self.party_attribute_box.clear()
        self.party_attribute_box.setLayer(self.layer)

        self.location_attribute_box.clear()
        self.location_attribute_box.setLayer(self.layer)

        self.relationship_attribute_box.clear()
        self.relationship_attribute_box.setLayer(self.layer)

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.project = self.parent.project

        if not self.layer or self.layer != self.parent.layer:
            self.layer = self.parent.layer
            self.set_attributes_box()

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return self.parent.step_project_update05
