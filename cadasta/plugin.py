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
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import (
    QAction,
    QIcon
)
from qgis.core import QgsMapLayerRegistry
# Initialize Qt resources from file resources.py
# Import the code for the dialog
from cadasta.gui.tools.cadasta_dialog import CadastaDialog
from cadasta.gui.tools.widget.contact_widget import ContactWidget
from cadasta.gui.tools.widget.options_widget import OptionsWidget
from cadasta.gui.tools.wizard.project_creation_wizard import (
    ProjectCreationWizard
)
from cadasta.gui.tools.wizard.project_download_wizard import (
    ProjectDownloadWizard
)
from cadasta.gui.tools.wizard.project_update_wizard import (
    ProjectUpdateWizard
)
from cadasta.gui.tools.helper.helper_dialog import (
    HelperDialog
)
from cadasta.gui.tools.about.about_dialog import (
    AboutDialog
)
from cadasta.common.setting import get_authtoken, get_user_organizations

# Initialize Qt resources from file resources.py
# Import the code for the dialog
from cadasta.utilities.resources import resources_path
from cadasta.utilities.utilities import Utilities

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
        self.project_download_wizard = None
        self.project_creation_wizard = None
        self.project_update_wizard = None
        self.questionnaire_update_wizard = None
        self.wizard = None

        registry = QgsMapLayerRegistry.instance()
        registry.layerWillBeRemoved.connect(self.layer_removed)
        registry.layerWasAdded.connect(self.layer_added)

        # Declare instance attributes
        self.actions = []

    def layer_removed(self, layer_id):
        """Function that triggered when layer removed.

        :param layer_id: Removed layer id.
        :type layer_id: QString
        """
        layer = QgsMapLayerRegistry.instance().mapLayer(layer_id)
        layer_names = layer.name().split('/')
        if len(layer_names) > 1 and \
                ('relationships' in layer.name() or 'parties' in layer.name()):
            try:
                project_slug, attribute = layer_names[1].split('_')
                organization_slug = layer_names[0]
                Utilities.add_tabular_layer(
                    layer,
                    organization_slug,
                    project_slug,
                    attribute)
                self.project_update_wizard.setEnabled(False)
            except ValueError:
                return

    def layer_added(self, layer):
        """Function that triggered when layer was added.

        :param layer: Added layer.
        :type layer: QgsVectorLayer
        """

        # Load csv file
        layer_names = layer.name().split('/')
        if len(layer_names) > 1 and \
                ('relationships' in layer.name() or 'parties' in layer.name()):
            try:
                project_slug, attribute = layer_names[1].split('_')
                organization_slug = layer_names[0]
                Utilities.load_csv_file_to_layer(
                    layer,
                    organization_slug,
                    project_slug,
                    attribute)
                self.layer_changed(layer)
            except ValueError:
                return

    def layer_changed(self, layer):
        """Function that triggered when layer changed.

        :param layer: New layer that selected.
        :type layer: QgsVectorLayer
        """
        if get_authtoken() and layer:
            if 'parties' in layer.name() or 'relationships' in layer.name():
                layer_names = layer.name().split('/')
                organization_slug = layer_names[0]
                project_slug = layer_names[1].split('_')[0]
                if organization_slug and project_slug:
                    information = Utilities.get_basic_information(
                        organization_slug=organization_slug,
                        project_slug=project_slug
                    )
                else:
                    self.project_update_wizard.setEnabled(False)
                    return
            else:
                information = Utilities.get_basic_information_by_vector(layer)
            if information:
                try:
                    organization_slug = information['organization']['slug']
                    if organization_slug in get_user_organizations():
                        self.project_update_wizard.setEnabled(True)
                        return
                except TypeError:
                    pass
        self.project_update_wizard.setEnabled(False)

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

        if add_to_menu:
            pass

        if add_to_toolbar:
            pass

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self._create_options_dialog()
        self._create_project_download_wizard()
        self._create_project_creation_wizard()
        self._create_project_update_wizard()
        self._create_contact_dialog()
        self._create_help_dialog()
        self._create_about_dialog()
        for action in self.actions:
            self.iface.addPluginToVectorMenu(
                self.tr(u'&Cadasta'),
                action)

        self.project_update_wizard.setEnabled(False)
        if get_authtoken():
            self._enable_authenticated_menu()
        else:
            self._disable_authenticated_menu()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        if self.wizard:
            self.wizard.deleteLater()
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Cadasta'),
                action)

    # ------------------------------------------------------------------------
    # initiate option dialog
    # ------------------------------------------------------------------------
    def _create_options_dialog(self):
        """Create action for options dialog."""
        icon_path = resources_path('images', 'cadasta-options-64.png')
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Options'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_options_dialog
        )

    def show_options_dialog(self):
        """Show the options dialog."""
        dialog = CadastaDialog(
            iface=self.iface,
            subtitle=self.tr(u'Cadasta Options'),
            widget=OptionsWidget()
        )

        dialog.widget.authenticated.connect(self._enable_authenticated_menu)
        dialog.widget.unauthenticated.connect(
            self._disable_authenticated_menu)

        dialog.show()
        dialog.exec_()

    def _enable_authenticated_menu(self):
        """Enable menu that requires auth token to proceed."""
        self.project_creation_wizard.setEnabled(True)
        if len(self.iface.legendInterface().selectedLayers()) > 0:
            self.layer_changed(
                self.iface.legendInterface().selectedLayers()[0])
        else:
            self.layer_changed(None)

    def _disable_authenticated_menu(self):
        """Disable menu that requires auth token to proceed."""
        self.project_creation_wizard.setEnabled(False)
        self.project_update_wizard.setEnabled(False)

    # ------------------------------------------------------------------------
    # initiate project creation dialog
    # ------------------------------------------------------------------------
    def _create_project_creation_wizard(self):
        """Create action for project creation wizard."""
        icon_path = resources_path('images', 'cadasta-create-64.png')
        self.project_creation_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Create Project'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_project_creation_wizard
        )

    def show_project_creation_wizard(self):
        """Show the project creation wizard."""
        dialog = ProjectCreationWizard(
            iface=self.iface
        )
        self.wizard = dialog
        dialog.show()
        dialog.exec_()

    # ------------------------------------------------------------------------
    # initiate project download dialog
    # ------------------------------------------------------------------------
    def _create_project_download_wizard(self):
        """Create action for project download wizard."""
        icon_path = resources_path('images', 'cadasta-download-64.png')
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Download Project'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_project_download_wizard
        )

    def show_project_download_wizard(self):
        """Show the project download wizard."""
        dialog = ProjectDownloadWizard(
            iface=self.iface
        )
        dialog.show()
        dialog.exec_()

    # ------------------------------------------------------------------------
    # initiate update project dialog
    # ------------------------------------------------------------------------
    def _create_project_update_wizard(self):
        """Create action for project update wizard."""
        icon_path = resources_path('images', 'cadasta-update-64.png')
        self.project_update_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Update Project'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_project_update_wizard
        )

    def show_project_update_wizard(self):
        """Show the project update dialog."""
        dialog = ProjectUpdateWizard(
            iface=self.iface
        )
        dialog.show()
        dialog.exec_()

    # ------------------------------------------------------------------------
    # initiate contact dialog
    # ------------------------------------------------------------------------
    def _create_contact_dialog(self):
        """Create action for contact."""
        icon_path = resources_path('images', 'cadasta-contact-64.png')
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Contact'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_contact_dialog
        )

    def show_contact_dialog(self):
        """Show the contact dialog."""
        dialog = CadastaDialog(
            iface=self.iface,
            subtitle='Contact',
            widget=ContactWidget()
        )
        dialog.show()
        dialog.exec_()

    # ------------------------------------------------------------------------
    # initiate help dialog
    # ------------------------------------------------------------------------
    def _create_help_dialog(self):
        """Create action for help diaog."""
        icon_path = resources_path('images', 'casdasta-help-64.png')
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'Help'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_help_dialog
        )

    def show_help_dialog(self):
        """Show the help dialog."""
        dialog = HelperDialog(
            iface=self.iface
        )

        dialog.show()
        dialog.exec_()

    # ------------------------------------------------------------------------
    # initiate about dialog
    # ------------------------------------------------------------------------
    def _create_about_dialog(self):
        """Create action for help diaog."""
        icon_path = resources_path('images', 'icon.png')
        self.action_options_wizard = self.add_action(
            icon_path,
            text=self.tr(u'About'),
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            enabled_flag=True,
            callback=self.show_about_dialog
        )

    def show_about_dialog(self):
        """Show the help dialog."""
        dialog = AboutDialog(
            iface=self.iface
        )
        dialog.show()
        dialog.exec_()
