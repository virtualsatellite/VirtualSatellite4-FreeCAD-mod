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

ICON_WORKBENCH = 'VirtualSatelliteWorkbench.svg'

PATH_RESOURCE = "Resources"
PATH_ICONS = "Icons"

class Environment:
    '''
    
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
        This method hands back the resource path of the current module.
        '''
        path = os.path.join(cls.get_resource_path(), PATH_ICONS)
        return path

    @classmethod
    def get_icon_path(cls, iconName):
        '''
        This method hands back the resource path of the current module.
        '''
        path = os.path.join(cls.get_icons_path(), iconName)
        return path
