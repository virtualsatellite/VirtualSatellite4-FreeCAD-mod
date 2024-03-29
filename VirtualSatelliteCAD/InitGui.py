# -*- coding: utf-8 -*-
#
# Virtual Satellite 4 - FreeCAD module
#
# Copyright (C) 2019 by
#
#    DLR (German Aerospace Center),
#    Software for Space Systems and interactive Visualization
#    Braunschweig, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
from module.environment import Environment
import plugin.plugin_loader as loader
import os


class VirtualSatelliteWorkbench(Workbench):  # NOQA @UndefinedVariable
    '''
    This class initializes the Virtual Satellite Workbench in FreeCAD.
    It provides a new menu and some commands to import and export
    geometries from and to Virtual Satellite
    '''

    global FREECAD_MOD_VERSION
    FREECAD_MOD_VERSION = '0.2.0 Beta'

    def __init__(self, plugins):
        self.plugins = plugins

        import FreeCAD
        self.preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/VirtualSatelliteCAD")

        from module.environment import ICON_WORKBENCH, Environment  # NOQA 
        self.__class__.Icon = Environment().get_icon_path(ICON_WORKBENCH)
        self.__class__.MenuText = 'Virtual Satellite ' + FREECAD_MOD_VERSION
        self.__class__.ToolTip = 'Workbench for Virtual Satellite 4'

    def Initialize(self):
        # Required method by FreeCAD framework
        # This import has to happen here, moving on the top does not
        # work as expected. This is due to some FreeCAD internals
        from commands.command_import import CommandImport
        from commands.command_export import CommandExport
        from commands.command_about import CommandAbout
        from commands.command_definitions import COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE
        from commands.command_definitions import COMMAND_ID_IMPORT_2_FREECAD
        from commands.command_definitions import COMMAND_ID_ABOUT

        toolbarCommands = [COMMAND_ID_IMPORT_2_FREECAD, COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE]
        menuCommands = [COMMAND_ID_IMPORT_2_FREECAD, COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE, COMMAND_ID_ABOUT]

        displayName = 'VirtualSatelliteMod'
        self.appendToolbar(displayName, toolbarCommands)
        self.appendMenu(displayName, menuCommands)

        Gui.addCommand(COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE, CommandExport(self))  # NOQA @UndefinedVariable
        Gui.addCommand(COMMAND_ID_IMPORT_2_FREECAD, CommandImport(self))  # NOQA @UndefinedVariable
        Gui.addCommand(COMMAND_ID_ABOUT, CommandAbout())  # NOQA @UndefinedVariable

    def GetClassName(self):
        # Required method by FreeCAD framework
        return "Gui::PythonWorkbench"

    def getActivePlugin(self):

        for plugin in self.plugins:
            isSelected = self.preferences.GetBool(plugin.name)
            if isSelected:
                return plugin

        # Inform the user that he has to select an active plugin
        from PySide2.QtWidgets import QMessageBox
        msgBox = QMessageBox()
        msgBox.setText('No Plugin selected!')
        msgBox.setInformativeText('Please select one in the preferences!')
        msgBox.exec_()
        return None


# First load the plugins that are required in workbench and settings
loader.load_plugins(Environment().get_module_path())

# Finally add the Virtual Satellite Workbench to the FreeCAD application
Gui.addWorkbench(VirtualSatelliteWorkbench(loader.plugins))  # NOQA @UndefinedVariable

# Build the preferences ui
preferences_ui = ""
with open(Environment().get_ui_path('preferences_header.ui'), 'r') as file:
    preferences_ui += file.read()

# Build general uis plugin selection
with open(Environment().get_ui_path('preferences_plugin_radiobutton.ui'), 'r') as file:
    TEMPLATE = file.read()

# For each plugin create a radiobutton
for i, plugin in enumerate(loader.plugins):
    ui = TEMPLATE
    ui = ui.replace('ID', str(i))
    ui = ui.replace('PLUGIN_NAME', plugin.name)
    preferences_ui += ui

with open(Environment().get_ui_path('preferences_footer.ui'), 'r') as file:
    preferences_ui += file.read()

with open(Environment().get_ui_path('preferences.ui'), 'w') as file:
    file.write(preferences_ui)

# Add the preferences page
Gui.addIconPath(Environment().get_icons_path())  # NOQA @UndefinedVariable
Gui.addPreferencePage(Environment().get_ui_path('preferences.ui'), 'Virtual Satellite')  # NOQA @UndefinedVariable

# Add custom plugin UI
for plugin in loader.plugins:
    if(plugin.hasPreferencesUi):
        Gui.addPreferencePage(os.path.join(Environment().get_plugin_path(plugin.directory), 'preferences.ui'), 'Virtual Satellite')  # NOQA @UndefinedVariable
