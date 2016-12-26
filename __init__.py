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

from qgis.PyQt.QtCore import (
    QLocale,
    QTranslator,
    QCoreApplication,
    QSettings)

# Setup internationalisation for the plugin.
#
# See if QGIS wants to override the system locale
# and then see if we can get a valid translation file
# for whatever locale is effectively being used.

override_flag = QSettings().value(
    'locale/overrideFlag', True, type=bool)

if override_flag:
    locale_name = QSettings().value('locale/userLocale', 'en_US', type=str)
else:
    locale_name = QLocale.system().name()
    # NOTES: we split the locale name because we need the first two
    # character i.e. 'id', 'af, etc
    locale_name = str(locale_name).split('_')[0]

# Also set the system locale to the user overridden local
# so that the cadasta library functions gettext will work
# .. see:: :py:func:`common.utilities`
os.environ['LANG'] = str(locale_name)

root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
translation_path = os.path.join(
    root, 'i18n',
    str(locale_name) + '.qm')

if os.path.exists(translation_path):
    translator = QTranslator()
    result = translator.load(translation_path)
    if not result:
        message = 'Failed to load translation for %s' % locale_name
        raise Exception(message)
    # noinspection PyTypeChecker,PyCallByClass
    QCoreApplication.installTranslator(translator)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Cadasta class from file Cadasta.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from cadasta.plugin import CadastaPlugin
    return CadastaPlugin(iface)
