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

import os
import Init
import FreeCAD
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QFileDialog

ICON_WORKBENCH = 'VirtualSatelliteWorkbench2.svg'
ICON_IMPORT = 'VirtualSatelliteImport.svg'
ICON_EXPORT = 'VirtualSatelliteExport.svg'

PATH_RESOURCE = "Resources"
PATH_ICONS = "Icons"
PATH_TEST_RESOURCE = "Tests"
PATH_UI = "Ui"
PATH_PLUGINS = "plugins"


class Environment:
    '''
    This class helps to understand the environment where the module is executed in.
    E.g. knowing which is the directory of the module and so on
    '''

    @classmethod
    def get_module_path(cls):
        '''
        This method hands back the module path of the current module. Not
        just the module path of the executed FreeCAD
        '''
        path = os.path.dirname(Init.__file__)
        return path

    @classmethod
    def get_resource_path(cls):
        '''
        This method hands back the resource path of the current module.
        '''
        path = os.path.join(cls.get_module_path(), PATH_RESOURCE)
        return path

    @classmethod
    def get_icons_path(cls):
        '''
        This method hands back the icon resource path of the current module.
        '''
        path = os.path.join(cls.get_resource_path(), PATH_ICONS)
        return path

    @classmethod
    def get_icon_path(cls, icon_name):
        '''
        This method hands back the resource path of the named icon.
        '''
        path = os.path.join(cls.get_icons_path(), icon_name)
        return path

    @classmethod
    def get_tests_resource_path(cls):
        '''
        This method hands back the resource path of the named test resource.
        '''
        path = os.path.join(cls.get_resource_path(), PATH_TEST_RESOURCE)
        return path

    @classmethod
    def get_test_resource_path(cls, test_resource_name):
        '''
        This method hands back the resource path of the named test resource.
        '''
        path = os.path.join(cls.get_tests_resource_path(), test_resource_name)
        return path

    @classmethod
    def get_uis_path(cls):
        '''
        This method hands back the ui resource path of the current module.
        '''
        path = os.path.join(cls.get_resource_path(), PATH_UI)
        return path

    @classmethod
    def get_ui_path(cls, filename):
        '''
        This method hands back the resource path of the named ui.
        '''
        path = os.path.join(cls.get_uis_path(), filename)
        return path

    @classmethod
    def get_plugins_path(cls):
        '''
        This method hands back the plugin path of the current module.
        '''
        path = os.path.join(cls.get_module_path(), PATH_PLUGINS)
        return path

    @classmethod
    def get_plugin_path(cls, pluginname):
        '''
        This method hands back the path of the named plugin.
        '''
        path = os.path.join(cls.get_plugins_path(), pluginname)
        return path

    @classmethod
    def get_appdata_module_path(cls):
        '''
        This method hands back the module path of the local Appdata directory.
        '''
        return Init.APPDATA_DIR

    @classmethod
    def get_user_home_path(cls):
        '''
        This method hands back the home of the current user (e.g. documents)
        '''
        return FreeCAD.ConfigGet("UserHomePath")

    @classmethod
    def get_file_directory_path(cls):
        '''
        This method hands back the path of the directory to store freecad files to.
        Depending on the preferences it will either:
          Return the path specified via the preferences ui.
          If no valid directory is specified the user will be informed via a dialog
        Or:
          Open a directory selection dialog every time this method is called.
        '''
        preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/VirtualSatelliteCAD")
        usePref = preferences.GetBool("UseStaticFileDirectory")

        if usePref:
            path = preferences.GetString("FileDirectory")

            if not os.path.isdir(path):
                msgBox = QMessageBox()
                msgBox.setText('No valid directory to store FreeCAD files (.FCstd) specified.')
                msgBox.setInformativeText(
                    f'\'{path}\' is not a valid directory.\n' +
                    'Please specify one in the preferences.')
                msgBox.exec_()
                return None

        else:
            path = QFileDialog.getExistingDirectory(
                None,
                "Open directory for FreeCAD files (.FCstd) (can be disabled in preferences)",
                cls.get_user_home_path())

        return path
