# coding=utf-8
"""
Cadasta **Cadasta Project Update Dialog.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging

from cadasta.gui.tools.wizard.step_project_update01 import (
    StepProjectUpdate01
)
from cadasta.gui.tools.wizard.step_project_update02 import (
    StepProjectUpdate02
)
from cadasta.gui.tools.wizard.step_project_update03 import (
    StepProjectUpdate03
)

from cadasta.utilities.i18n import tr
from cadasta.gui.tools.wizard.wizard_dialog import WizardDialog

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ProjectUpdateWizard(WizardDialog):
    """Dialog implementation class for Project Update Wizard"""

    step_project_update01 = None
    step_project_update02 = None
    step_project_update03 = None

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
        super(ProjectUpdateWizard, self).__init__(parent, iface)

        self.project = None
        self.parties = None
        self.locations = None
        self.layer = None

        self.set_subtitle(
            tr('Cadasta project update wizard')
        )

    def first_step(self):
        """Returns the first step of wizard.

        :return: First step of wizard.
        :rtype: WizardStep
        """
        return self.step_project_update01

    def last_step(self):
        """Returns the last step of wizard.

        :return: Last step of wizard.
        :rtype: WizardStep
        """
        return self.step_project_update03

    def populate_stacked_widget(self):
        """Append widgets to stacked widget."""
        self.step_project_update01 = StepProjectUpdate01(self)
        self.step_project_update02 = StepProjectUpdate02(self)
        self.step_project_update03 = StepProjectUpdate03(self)

        self.stackedWidget.addWidget(self.step_project_update01)
        self.stackedWidget.addWidget(self.step_project_update02)
        self.stackedWidget.addWidget(self.step_project_update03)

    def prepare_the_next_step(self, new_step):
        """Prepare the next tab.

        :param new_step: New tab to be prepared.
        :type new_step: WizardStep
        """
        if new_step == self.step_project_update02:
            self.project = \
                self.step_project_update01.selected_project()
