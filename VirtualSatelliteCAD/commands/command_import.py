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
from commands.command_definitions import COMMAND_ID_IMPORT_2_FREECAD
from PySide2.QtWidgets import QFileDialog
from json_io.json_importer import JsonImporter


class CommandImport:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Calling the importer\n")

        path = FreeCAD.ConfigGet("UserAppData")

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getOpenFileName(
            None,  # ui parent
            "Open JSON file",  # dialog caption
            path,
            "JSON(*.json)")[0]  # filter

        if filename != '':
            FreeCAD.Console.PrintMessage(f"Successful read file '{filename}'\n")

            # TODO: where do we save the created FCstd files? AppData?
            # maybe create an subdir in AppData for VirSat stds?
            json_importer = JsonImporter(path)
            json_importer.fullImport(filename)

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_IMPORT),
                'MenuText': 'Import to Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json import.'}


FreeCADGui.addCommand(COMMAND_ID_IMPORT_2_FREECAD, CommandImport())  # @UndefinedVariable
