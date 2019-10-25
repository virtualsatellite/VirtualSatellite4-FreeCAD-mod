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

import FreeCAD
import FreeCADGui
from module.environment import Environment, ICON_IMPORT
from commands.command_definitions import COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE


class CommandExport:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Calling the importer\n")

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_IMPORT),
                'MenuText': 'Import from Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json import.'}


FreeCADGui.addCommand(COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE, CommandExport())  # @UndefinedVariable
