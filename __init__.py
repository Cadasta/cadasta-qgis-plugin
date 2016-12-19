# -*- coding: utf-8 -*-
"""
This tool helps create, update, upload and download Cadasta projects.
 - **Module cadasta.**

This script initializes the plugin, making it known to QGIS.

Contact : christian@kartoza.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import sys
import os

__copyright__ = "Copyright 2016, Cadasta Project"
__license__ = "GPL version 3"
__email__ = "christian@kartoza.com"
__revision__ = '$Format:%H$'


sys.path.append(os.path.dirname(__file__))


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Cadasta class from file Cadasta.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from cadasta.plugin import CadastaPlugin
    return CadastaPlugin(iface)
