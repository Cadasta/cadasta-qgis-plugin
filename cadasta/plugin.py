# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Cadasta
                                 A QGIS plugin
 This tool helps create, update, upload and download Cadasta projects.
                              -------------------
        begin                : 2016-11-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Kartoza
        email                : christian@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import logging
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QAction, QIcon, QMenu, QWidget
# Initialize Qt resources from file resources.py
# Import the code for the dialog
from cadasta.gui.tools.cadasta_login import CadastaLogin
from cadasta.gui.tools.cadasta_project_download_step_1 import (
    CadastaProjectDownloadStep1
)
import os.path

LOGGER = logging.getLogger('CadastaQGISPlugin')


class CadastaPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.action_options_wizard = None
        self.wizard = None
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Cadasta_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Cadasta QGIS plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Cadasta')
        self.toolbar.setObjectName(u'Cadasta')

        # Create menu
        self.main_menu = QMenu(
            self.tr(u'&Cadasta'),
            self.iface.mainWindow().menuBar()
        )
        menu_actions = self.iface.mainWindow().menuBar().actions()

        # Add cadasta menu to second last position of menu bar
        last_action = menu_actions[-1]
        self.iface.mainWindow().menuBar().insertMenu(
            last_action,
            self.main_menu
        )

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Cadasta', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.main_menu.addAction(action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self._create_options_wizard_action()
        self._create_project_download_wizard_action()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        if self.wizard:
            self.wizard.deleteLater()
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Cadasta QGIS plugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        self.iface.mainWindow().removeToolBar(self.toolbar)

    def _create_options_wizard_action(self):
        """Create action for options wizard."""
        icon_path = ':/plugins/cadasta-qgis-plugin/icon.png'
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Options'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_options_wizard
        )

    def show_options_wizard(self):
        """Show the options wizard."""
        dialog = CadastaLogin()
        dialog.show()
        dialog.exec_()

    def _create_project_download_wizard_action(self):
        """Create action for project download wizard."""
        icon_path = ':/plugins/cadasta-qgis-plugin/icon.png'
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Project Download'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_project_download_wizard
        )

    def show_project_download_wizard(self):
        """Show the project download wizard."""
        dialog = CadastaProjectDownloadStep1()
        dialog.show()
        dialog.exec_()
