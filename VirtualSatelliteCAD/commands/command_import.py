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
from module.environment import Environment, ICON_IMPORT
from json_io.json_importer import JsonImporter
import os

Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Log = FreeCAD.Console.PrintLog


class CommandImport:

    def __init__(self, workbench):
        self.workbench = workbench

    def Activated(self):
        Msg("Calling the importer\n")

        file_directory_path = Environment.get_file_directory_path()
        if file_directory_path is None:
            return

        # call the import from the plugin
        json_object = self.workbench.getActivePlugin().importToDict(file_directory_path)

        if(json_object is None):
            Err("Plugin import returned None\n")
            return
        else:
            Log("Plugin returned following JSON:\n")
            Log("{}\n".format(json_object))

        json_importer = JsonImporter(file_directory_path + os.sep)
        json_importer.full_import(json_object)
        Msg("Finished import\n")

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_IMPORT),
                'MenuText': 'Import to Virtual Satellite',
                'ToolTip': 'Open the dialog for the Virtual Satellite json import.'}
