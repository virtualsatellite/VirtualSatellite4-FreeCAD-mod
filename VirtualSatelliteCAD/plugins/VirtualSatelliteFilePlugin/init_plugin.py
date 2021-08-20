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
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin

Log = FreeCAD.Console.PrintMessage


@Plugin.register
class VirSatFilePlugin(Plugin):
    '''
    Legacy Plugin that directly im-/exports a JSON file
    '''
    def importToDict(self):
        from PySide2.QtWidgets import QFileDialog
        from module.environment import Environment
        import json

        file_directory_path = Environment.get_file_directory_path()
        if file_directory_path is None:
            return

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getOpenFileName(
            None,  # ui parent
            "Open JSON file",  # dialog caption
            file_directory_path,
            "JSON(*.json)")[0]

        if filename != '':
            (f"Selected file '{filename}'\n")

            with open(filename, 'r') as f:
                try:
                    return json.load(f)
                except ValueError as error:
                    Log(f"ERROR: Invalid JSON found: '{error}'\n")
                    Log("Please provide a valid JSON\n")
        return

    def exportFromDict(self, data_dict):
        from PySide2.QtWidgets import QFileDialog
        from module.environment import Environment
        import json

        file_directory_path = Environment.get_file_directory_path()
        if file_directory_path is None:
            return

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getSaveFileName(
            None,  # ui parent
            "Save JSON file",  # dialog caption
            file_directory_path,
            "JSON(*.json)")[0]
        if filename != '':
            json_str = json.dumps(data_dict)

            with open(filename, 'w') as file:
                file.write(json_str)


register_plugin(VirSatFilePlugin("Virtual Satellite File Plugin (Legacy)", "VirtualSatelliteFilePlugin", False))
