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
import json
from freecad.active_document import ActiveDocument

Log = FreeCAD.Console.PrintMessage


class CommandExport:
    def Activated(self):
        Log("Calling the exporter\n")

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getSaveFileName(
            None,  # ui parent
            "Save JSON file",  # dialog caption
            Environment.get_appdata_module_path(),
            "JSON(*.json)")[0]  # filter

        if filename != '':
            json_exporter = JsonExporter(Environment.get_appdata_module_path())
            # TODO: better way to do this?, fix
            if(FreeCAD.ActiveDocument is not None):
                active_document = ActiveDocument(Environment.get_appdata_module_path()).open_set_and_get_document(FreeCAD.ActiveDocument.Label)
                json_dict = json_exporter.full_export(active_document)
                json_str = json.dumps(json_dict)

                with open(filename, 'w') as file:
                    file.write(json_str)
            else:
                print("Error msg")

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_EXPORT),
                'MenuText': 'Export from Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json export.'}


FreeCADGui.addCommand(COMMAND_ID_EXPORT_2_VIRTUAL_SATELLITE, CommandExport())  # @UndefinedVariable
