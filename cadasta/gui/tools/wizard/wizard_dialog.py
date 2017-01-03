# coding=utf-8
"""
Cadasta **Cadasta Wizard Dialog.**

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
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import pyqtSignature
from cadasta.utilities.resources import get_ui_class, resources_path
from cadasta.utilities.i18n import tr

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_ui_class('wizard/wizard_dialog_base.ui')

LOGGER = logging.getLogger('CadastaQGISPlugin')


class WizardDialog(QDialog, FORM_CLASS):
    """Dialog implementation class for Wizard"""

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

        self.iface = iface
        self.parent_step = None
        self.message_bar = None

        self.steps = []

        self.set_logo()
        self.populate_stacked_widget()
        self.update_step_label()

        first_step = self.first_step()
        first_step.set_widgets()
        self.go_to_step(first_step)

    def last_step(self):
        """Returns the last step of wizard.

        This method must be implemented in derived classes.

        :returns: Last step of wizard.
        :rtype: WizardStep
        """
        raise NotImplementedError("The current wizard class doesn't implement \
                                    the populate_stacked_widget method")

    def first_step(self):
        """Returns the first step of wizard.

        This method must be implemented in derived classes.

        :returns: First step of wizard.
        :rtype: WizardStep
        """
        raise NotImplementedError("The current wizard class doesn't implement \
                                    the populate_stacked_widget method")

    def populate_stacked_widget(self):
        """Append widgets to stacked widget.

        This method must be implemented in derived classes.
        """
        raise NotImplementedError("The current wizard class doesn't implement \
                            the populate_stacked_widget method")

    def update_step_label(self):
        """Update step label with current step / total step."""
        current_step = self.stackedWidget.currentIndex()
        total_step = self.stackedWidget.count()

        self.label_step.setText('%d/%d' % (current_step + 1, total_step))

    def set_subtitle(self, subtitle):
        """Set subtitle of dialog.

        :param subtitle: Subtitle string
        :type subtitle: str
        """
        self.label_subtitle.setText(subtitle)

    def set_logo(self):
        """Set logo of dialog."""
        filename = resources_path('images', 'white_icon.png')
        pixmap = QPixmap(filename)
        self.label_main_icon.setPixmap(pixmap)

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
        self.update_step_label()

        # Enable the Back button unless it's not the first step or
        # last step
        self.back_button.setEnabled(
                step not in [self.first_step()] or
                self.parent_step is not None)

        # Set Next button label
        if step == self.last_step():
            self.next_button.setText(self.tr('Close'))
        else:
            self.next_button.setText(self.tr('Next'))

    def get_current_step(self):
        """Return current step of the wizard.

        :returns: Current step of the wizard.
        :rtype: WizardStep instance
        """
        return self.stackedWidget.currentWidget()

    def prepare_the_next_step(self, new_step):
        """Prepare the next tab.

        To be implemented in derived classes.

        :param new_step: New tab to be prepared.
        :type new_step: WizardStep
        """
        pass

    def prepare_the_previous_step(self, previous_step):
        """Prepare the previous tab.

        :param previous_step: New tab to be prepared.
        :type previous_step: WizardStep
        """
        self.next_button.setEnabled(True)

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
            self.prepare_the_next_step(new_step)
            new_step.set_widgets()
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
        self.prepare_the_previous_step(previous_step)
        self.go_to_step(previous_step)

    # prevents actions being handled twice
    # noinspection PyPep8Naming
    @pyqtSignature('')
    def on_cancel_button_released(self):
        """Handle the Cancel button release.

        .. note:: This is an automatic Qt slot
           executed when the Back button is released.
        """
        self.close()
