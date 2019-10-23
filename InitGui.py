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

class VirtualSatelliteWorkbench(Workbench):  # NOQA @UndefinedVariable
    '''
    This class initializes the Virtual Satellite Workbench in FreeCAD.
    It provides a new menu and some commands to import and export
    geometries from and to Virtual Satellite
    '''

    def __init__(self):
        from module.environment import ICON_WORKBENCH, Environment
        self.__class__.Icon = Environment().get_icon_path(ICON_WORKBENCH)
        self.__class__.MenuText = 'Virtual Satellite'
        self.__class__.ToolTip = 'Virtual Satellite 4 Workbench'

    def Initialize(self):
        # Required method by FreeCAD framework
        # This import has to happen here, moving on the top does not
        # work as expected. This is due to some FreeCAD internals
        import commands.command_import  # NOQA @UnusedImport
        import commands.command_export  # NOQA @UnusedImport
        from commands.command_definitions import COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE
        from commands.command_definitions import COMMAND_ID_IMPORT_2_FREECAD
        self.appendToolbar('VirtualSatelliteMod', [COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE])
        self.appendMenu('VirtualSatelliteMod', [COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE])
        self.appendToolbar('VirtualSatelliteMod', [COMMAND_ID_IMPORT_2_FREECAD])
        self.appendMenu('VirtualSatelliteMod', [COMMAND_ID_IMPORT_2_FREECAD])

    def GetClassName(self):
        # Required method by FreeCAD framework
        return "Gui::PythonWorkbench"


# Finally add the Virtual Satellite Workbench to the FreeCAD application
Gui.addWorkbench(VirtualSatelliteWorkbench())  # NOQA @UndefinedVariable
