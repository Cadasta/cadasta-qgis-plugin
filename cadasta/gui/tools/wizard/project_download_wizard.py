# coding=utf-8
"""
Cadasta **Cadasta Project Download Dialog.**

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
from qgis.PyQt.QtCore import pyqtSignature
from qgis.gui import QgsMessageBar
from step_project_download01 import StepProjectDownload01
from step_project_download02 import StepProjectDownload02

from cadasta.utilities.resources import get_ui_class, resources_path
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('wizard/wizard_dialog_base.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class ProjectDownloadWizard(QDialog, FORM_CLASS):
    """Dialog implementation class for Project Download Wizard"""

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
        self.step_length = 2
        self.set_step_label()
        self.message_bar = None

        self.step_project_download01 = StepProjectDownload01(self)
        self.step_project_download02 = StepProjectDownload02(self)

        self.stackedWidget.addWidget(self.step_project_download01)
        self.stackedWidget.addWidget(self.step_project_download02)

        self.steps = []

        step = self.step_project_download01
        step.set_widgets()
        self.go_to_step(step)
        self.set_logo()

    def set_logo(self):
        """Set logo of dialog."""
        filename = resources_path('images', 'white_icon.png')
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

        # Enable the Back button unless it's not the first step or
        # last step
        self.back_button.setEnabled(
            step not in [self.step_project_download01] or
            self.parent_step is not None)

        # Set Next button label
        if step == self.step_project_download02:
            self.next_button.setText(self.tr('Close'))
        else:
            self.next_button.setText(self.tr('Next'))

    def get_current_step(self):
        """Return current step of the wizard.

        :returns: Current step of the wizard.
        :rtype: WizardStep instance
        """
        return self.stackedWidget.currentWidget()

    # prevents actions being handled twice
    # noinspection PyPep8Naming
    @pyqtSignature('')
    def on_next_button_released(self):
        """Handle the Next button release.

        .. note:: This is an automatic Qt slot
           executed when the Next button is released.
        """
        current_step = self.get_current_step()
        valid_status, message = current_step.validate_step()

        if not valid_status:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                tr('Error'),
                message
            )
            LOGGER.info(message)
            return

        self.steps.append(current_step)

        # Determine the new step to be switched
        new_step = current_step.get_next_step()

        if new_step is not None:
            # Prepare the next tab
            if new_step == self.step_project_download02:
                new_step.project = \
                    self.step_project_download01.selected_project()
            new_step.set_widgets()
            self.step_index += 1
            self.set_step_label()
        else:
            # Wizard complete
            self.accept()
            return

        self.go_to_step(new_step)

    # prevents actions being handled twice
    # noinspection PyPep8Naming
    @pyqtSignature('')
    def on_back_button_released(self):
        """Handle the Back button release.

        .. note:: This is an automatic Qt slot
           executed when the Back button is released.
        """
        previous_step = self.steps.pop()
        self.next_button.setEnabled(True)
        self.step_index -= 1
        self.set_step_label()
        self.go_to_step(previous_step)
