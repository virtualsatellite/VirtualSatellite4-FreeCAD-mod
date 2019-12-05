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
from module.environment import Environment, ICON_EXPORT
from commands.command_definitions import COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE
from PySide2.QtWidgets import QFileDialog
from json_io.json_exporter import JsonExporter

Log = FreeCAD.Console.PrintMessage


class CommandExport:
    def Activated(self):
        Log("Calling the importer\n")

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getSaveFileName(
            None,  # ui parent
            "Save JSON file",  # dialog caption
            Environment.get_appdata_module_path(),
            "JSON(*.json)")[0]  # filter

        if filename != '':
            with open(filename, 'w') as file:

                json_exporter = JsonExporter()
                json_str = json_exporter.full_export()

                file.write(json_str)

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_EXPORT),
                'MenuText': 'Export from Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json export.'}


FreeCADGui.addCommand(COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE, CommandExport())  # @UndefinedVariable
