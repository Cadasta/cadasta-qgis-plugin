# coding=utf-8
"""Common functionality used by regression tests."""

import os
import sys
import logging
from qgis.utils import iface


LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None
GEOCRS = 4326  # constant for EPSG:GEOCRS Geographic CRS id
GOOGLECRS = 3857  # constant for EPSG:GOOGLECRS Google Mercator id
DEVNULL = open(os.devnull, 'w')


def get_qgis_app():
    """ Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """
    global QGIS_APP, PARENT, IFACE, CANVAS  # pylint: disable=W0603

    if iface:
        from qgis.core import QgsApplication
        QGIS_APP = QgsApplication
        CANVAS = iface.mapCanvas()
        PARENT = iface.mainWindow()
        IFACE = iface
        return QGIS_APP, CANVAS, IFACE, PARENT

    try:
        from qgis.PyQt import QtGui, QtCore
        from qgis.core import QgsApplication
        from qgis.gui import QgsMapCanvas
        from qgis_interface import QgisInterface
        # noinspection PyPackageRequirements
        from qgis.PyQt.QtCore import QCoreApplication, QSettings
    except ImportError:
        return None, None, None, None

    if QGIS_APP is None:

        # noinspection PyCallByClass,PyArgumentList
        QCoreApplication.setOrganizationName('QGIS')
        # noinspection PyCallByClass,PyArgumentList
        QCoreApplication.setOrganizationDomain('qgis.org')
        # noinspection PyCallByClass,PyArgumentList
        QCoreApplication.setApplicationName('QGIS2CadastaTesting')

        gui_flag = True  # All test will run qgis in gui mode

        # noinspection PyPep8Naming
        if 'argv' in dir(sys):
            QGIS_APP = QgsApplication(sys.argv, gui_flag)
        else:
            QGIS_APP = QgsApplication([], gui_flag)

        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)

    if PARENT is None:
        # noinspection PyPep8Naming
        PARENT = QtGui.QWidget()

    if CANVAS is None:
        # noinspection PyPep8Naming
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(400, 400))

    if IFACE is None:
        # QgisInterface is a stub implementation of the QGIS plugin interface
        # noinspection PyPep8Naming
        IFACE = QgisInterface(CANVAS)

    return QGIS_APP, CANVAS, IFACE, PARENT
