# coding=utf-8
"""
Cadasta project creation step -**Cadasta Wizard**

This module provides: Project Creation Step 3 : Upload to cadasta

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import json
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)


class StepProjectCreation3(WizardStep, FORM_CLASS):
    """Step 3 for project creation"""

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.textEdit.setText(
            json.dumps(self.parent.get_all_data(), sort_keys=True,
                       indent=4, separators=(',', ': '))
        )

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
        return None
