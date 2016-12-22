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
    """Step 1 for project creation"""

    layer = None

    def set_widgets(self):
        """Set all widgets on the tab."""
        layer = self.layer
        field_names = [field.name() for field in layer.pendingFields()]

        if 'id' in field_names:
            field_names.remove(u'id')

        field_names.insert(0, ' ')

        # Location Attribute
        self.cbxLocAttr.addItems(field_names)
        # Location Type
        self.cbxLocType.addItems(field_names)
        # Party Name
        self.cbxPartyName.addItems(field_names)
        # Relationship Type
        self.cbxRelType.addItems(field_names)
        # Party Type
        self.cbxPartyType.addItems(field_names)
        # Party Attribute
        self.cbxPartyAttr.addItems(field_names)
        # Relationship Attribute
        self.cbxRelAttr.addItems(field_names)
