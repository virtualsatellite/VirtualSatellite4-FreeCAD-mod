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

    # TODO: Update user file handling
    @classmethod
    def get_appdata_module_path(cls):
        '''
        This method hands back the module path of the local Appdata directory.
        '''
        return Init.APPDATA_DIR
