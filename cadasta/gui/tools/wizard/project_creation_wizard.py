# coding=utf-8
"""
Cadasta **Cadasta project creation Dialog.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging

from cadasta.gui.tools.wizard.step_project_creation01 import (
    StepProjectCreation1
)
from cadasta.gui.tools.wizard.step_project_creation02 import (
    StepProjectCreation2
)
from cadasta.gui.tools.wizard.step_project_creation03 import (
    StepProjectCreation3
)

from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_dialog import WizardDialog

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ProjectCreationWizard(WizardDialog):
    """Dialog implementation class for Project Creation Wizard"""

    step_project_creation01 = None
    step_project_creation02 = None
    step_project_creation03 = None

    def __init__(self, parent=None, iface=None):
        """Constructor for the dialog.

        .. note:: In QtDesigner the advanced editor's predefined keywords
           list should be shown in english always, so when adding entries to
           cboKeyword, be sure to choose :safe_qgis:`Properties<<` and untick
           the :safe_qgis:`translatable` property.

        :param parent: Parent widget of this dialog.
        :type parent: QWidget

        :param iface: QGIS QGisAppInterface instance.
        :type iface: QGisAppInterface
        """
        super(ProjectCreationWizard, self).__init__(parent, iface)

        self.set_subtitle(
            tr('Cadasta project creation wizard')
        )
        self.layer = None

    def first_step(self):
        """Returns the first step of wizard.

        :returns: First step of wizard.
        :rtype: WizardStep
        """
        return self.step_project_creation01

    def last_step(self):
        """Returns the last step of wizard.

        :returns: Last step of wizard.
        :rtype: WizardStep
        """
        return self.step_project_creation03

    def populate_stacked_widget(self):
        """Append widgets to stacked widget."""
        self.step_project_creation01 = StepProjectCreation1(self)
        self.step_project_creation02 = StepProjectCreation2(self)
        self.step_project_creation03 = StepProjectCreation3(self)

        self.stackedWidget.addWidget(self.step_project_creation01)
        self.stackedWidget.addWidget(self.step_project_creation02)
        self.stackedWidget.addWidget(self.step_project_creation03)

    # ===========================
    # NAVIGATION
    # ===========================

    def prepare_the_next_step(self, new_step):
        """Prepare the next tab.

        :param new_step: New tab to be prepared.
        :type new_step: WizardStep
        """
        if new_step == self.step_project_creation02:
            self.layer = self.step_project_creation01.selected_layer()

    def step_1_data(self):
        """Returns step 1 data.

        :returns: Step 1 data
        :rtype: dict
        """
        return self.step_project_creation01.all_data()

    def step_2_data(self):
        """Returns step 2 data.

        :returns: Step 2 data
        :rtype: dict
        """
        return self.step_project_creation02.cadasta_fields()
