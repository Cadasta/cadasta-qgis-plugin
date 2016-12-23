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
import time
import logging
from qgis.PyQt.QtCore import pyqtSignature
from qgis.PyQt.QtCore import QEvent, QCoreApplication
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectCreation3(WizardStep, FORM_CLASS):
    """Step 3 for project creation"""

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.progress_bar.setVisible(False)
        self.lbl_status.setText(
            tr('Are you sure to upload the data?')
        )
        self.submit_button.clicked.connect(self.processing_data)

    def processing_data(self):
        """Processing data from all step"""
        self.progress_bar.setVisible(True)
        self.submit_button.setVisible(False)
        self.parent.pbnBack.setEnabled(False)

        self.lbl_status.setText(
            tr('Processing data')
        )

        data = dict()

        self.set_progress_bar(25)

        data['step_1'] = self.parent.step_1_data()
        self.set_progress_bar(50)

        data['step_2'] = self.parent.step_2_data()
        self.set_progress_bar(100)

        self.text_edit.setText(
            json.dumps(data, indent=4, separators=(',', ': '))
        )

        self.lbl_status.setText(
            tr('Finish')
        )

    def set_progress_bar(self, value):
        """Set progress bar value.

        :param value: integer value for progress bar
        :type value: int
        """
        self.progress_bar.setValue(value)
        QCoreApplication.processEvents()

    def upoading_data(self):
        """Uploading data to cadasta."""
        pass

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        return None
