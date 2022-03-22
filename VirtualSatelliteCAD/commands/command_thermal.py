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
from scripts.thermal.process_model import process_model
import os

Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Log = FreeCAD.Console.PrintLog


class CommandThermal:

    def __init__(self):
        pass

    def Activated(self):
        Msg("Calling the thermal concept scripts\n")

        from PySide2.QtWidgets import QFileDialog

        file_directory_path = Environment.get_file_directory_path()
        if file_directory_path is None:
            return

        directoryname = QFileDialog.getExistingDirectory(
            None,  # ui parent
            "Open directory with thermal information exported from Virtual Satellite",  # dialog caption
            file_directory_path)

        if directoryname != '':
            Msg(f"Selected directory '{directoryname}'\n")
            process_model(os.path.join(directoryname, ""))

        Msg("Finished thermal concept scripts\n")
        return

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_IMPORT),
                'MenuText': 'Execute thermal concept scripts',
                'ToolTip': 'Open the dialog for the Virtual Satellite thermal concept scripts.'}
