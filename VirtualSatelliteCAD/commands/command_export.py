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
import FreeCAD
from module.environment import Environment, ICON_EXPORT
from json_io.json_exporter import JsonExporter
from freecad.active_document import ActiveDocument

Log = FreeCAD.Console.PrintMessage


class CommandExport:

    def __init__(self, workbench):
        self.workbench = workbench

    def Activated(self):
        Log("Calling the exporter\n")

        file_directory_path = Environment.get_file_directory_path()
        if file_directory_path is None:
            return

        json_exporter = JsonExporter(file_directory_path + os.sep)

        if(FreeCAD.ActiveDocument is not None):
            # Export into the interim format
            document_name = FreeCAD.ActiveDocument.Label
            active_document = ActiveDocument(file_directory_path).open_set_and_get_document(document_name)
            json_dict = json_exporter.full_export(active_document)

            # call the export from the plugin
            self.workbench.getActivePlugin().exportFromDict(json_dict)

            # after export open the file again for the UI
            active_document = ActiveDocument(file_directory_path).open_set_and_get_document(document_name)

        else:
            Log("Error: First open a document to export it\n")

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_EXPORT),
                'MenuText': 'Export from Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json export.'}
