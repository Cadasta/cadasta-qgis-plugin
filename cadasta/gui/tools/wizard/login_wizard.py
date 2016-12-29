# coding=utf-8
"""
Cadasta **Cadasta Login Dialog.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging

from qgis.PyQt.QtGui import (
    QDialog,
    QPixmap
)
from step_login01 import StepLogin1

from cadasta.utilities.resources import get_ui_class, resources_path
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('wizard/wizard_dialog_base.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class LoginWizard(QDialog, FORM_CLASS):
    """Dialog implementation class for Login Wizard"""

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
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Cadasta')
        self.label_subtitle.setText(
            tr('Cadasta project download wizard')
        )

        self.iface = iface
        self.organisations_list = None
        self.layers = None
        self.parent_step = None
        self.step_index = 1
        self.step_length = 1
        self.set_step_label()
        self.message_bar = None

        self.step_login_1 = StepLogin1(self)

        self.stackedWidget.addWidget(self.step_login_1)

        self.steps = []

        step = self.step_login_1
        step.set_widgets()
        self.go_to_step(step)
        self.footerSection.setVisible(False)
        self.label_step.setVisible(False)
        self.set_logo()

    def set_logo(self):
        filename = resources_path('images/white_icon.png')
        LOGGER.debug(filename)
        pixmap = QPixmap(filename)
        self.label_main_icon.setPixmap(pixmap)

    def set_step_label(self):
        """Display step label."""
        self.label_step.setText('%d/%d' % (self.step_index, self.step_length))

    # ===========================
    # NAVIGATION
    # ===========================

    def go_to_step(self, step):
        """Set the stacked widget to the given step, set up the buttons,
           and run all operations that should start immediately after
           entering the new step.

        :param step: The step widget to be moved to.
        :type step: QWidget
        """
        self.stackedWidget.setCurrentWidget(step)

    def get_current_step(self):
        """Return current step of the wizard.

        :returns: Current step of the wizard.
        :rtype: WizardStep instance
        """
        return self.stackedWidget.currentWidget()
