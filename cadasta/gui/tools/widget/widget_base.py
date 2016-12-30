# coding=utf-8
"""
-**Cadasta Widget**

This module provides an abstract class for wizard steps

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import re
import os
import logging
# noinspection PyPackageRequirements
from qgis.PyQt.QtGui import QWidget

from cadasta.utilities.resources import get_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')


def get_widget_step_ui_class(py_file_name):
    """Get ui class based on python filename.

    Load a Qt Designer .ui file and return the generated form class and the Qt
    base class.
    .ui file is based on py filename.

    :param py_file_name: Filename of the widget
    :type py_file_name: str

    :return: Loaded .ui file
    :rtype: loaded ui
    """
    return get_ui_class(os.path.join(
        'widget', re.sub(r"pyc?$", "ui", os.path.basename(py_file_name))))


class WidgetBase(QWidget):
    """An abstract widget for cadasta."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.message_bar = None
