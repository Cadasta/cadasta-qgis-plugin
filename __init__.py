# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Cadasta
                                 A QGIS plugin
 This tool helps create, update, upload and download Cadasta projects.
                             -------------------
        begin                : 2016-11-25
        copyright            : (C) 2016 by Kartoza
        email                : christian@kartoza.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import sys
import os

sys.path.append(os.path.dirname(__file__))


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Cadasta class from file Cadasta.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .cadasta import Cadasta
    return Cadasta(iface)
