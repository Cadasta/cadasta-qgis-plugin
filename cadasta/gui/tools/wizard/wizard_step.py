# coding=utf-8
"""
-**Cadasta Wizard**

This module provides an abstract class for wizard steps

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import re
import os

# noinspection PyPackageRequirements
from PyQt4.QtGui import QWidget

from cadasta.utilities.resources import get_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'


def get_wizard_step_ui_class(py_file_name):
    return get_ui_class(os.path.join(
        'wizard', re.sub(r"pyc?$", "ui", os.path.basename(py_file_name))))


class WizardStep(QWidget):
    """An abstract step.
       Each step is a tab meant to be placed in the wizard.
       Each derived class must implement mandatory methods.
    """

    def __init__(self, parent=None):
        """Constructor

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def auto_select_one_item(self, list_widget):
        """Select item in the list in list_widget if it's the only item.

        :param list_widget: The list widget that want to be checked.
        :type list_widget: QListWidget
        """
        if list_widget.count() == 1 and list_widget.currentRow() == -1:
            list_widget.setCurrentRow(0)

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        return False, ''

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        raise NotImplementedError("The current step class doesn't implement \
            the get_next_step method")

    def set_widgets(self):
        """Set all widgets on the tab.

           This method must be implemented in derived classes.
        """
        raise NotImplementedError("The current step class doesn't implement \
            the set_widgets method")

    @property
    def step_type(self):
        """Whether it's a IFCW step or Keyword Wizard Step."""
        if 'stepfc' in self.__class__.__name__.lower():
            return 'step_fc'
        if 'stepkw' in self.__class__.__name__.lower():
            return 'step_kw'
