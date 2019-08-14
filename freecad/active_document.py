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
import FreeCADGui
import FreeCAD
import os

App = FreeCAD
Gui = FreeCADGui
Log = FreeCAD.Console.PrintLog
Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Wrn = FreeCAD.Console.PrintWarning

FREECAD_FILE_EXTENSION = ".FCstd"


class ActiveDocument(object):

    def __init__(self, working_directory):
        self._working_directory = working_directory

    def get_file_full_path(self, file_name_without_extension):
        part_file_fullpath = self._working_directory + file_name_without_extension + FREECAD_FILE_EXTENSION
        return part_file_fullpath

    def open_set_and_get_document(self, file_name_without_extension):

        file_full_path = self.get_file_full_path(file_name_without_extension)
        documents = list(App.listDocuments().keys())

        if documents.count(file_name_without_extension) == 0:
            if os.path.isfile(file_full_path):
                Log('Open existing FreeCAD file from disk for update...\n')
                App.open(file_full_path)
            else:
                Log('Create new FreeCAD file...\n')
                App.newDocument(file_name_without_extension)
        else:
            Log('Open existing already open FreeCAD file for update...\n')

        self.set_active_documents(file_name_without_extension)

        return self

    def set_active_documents(self, file_name_without_extension):
        App.setActiveDocument(file_name_without_extension)

        App.ActiveDocument = App.getDocument(file_name_without_extension)
        Gui.ActiveDocument = Gui.getDocument(file_name_without_extension)

        self.app_active_document = App.ActiveDocument
        self.gui_active_document = Gui.ActiveDocument

    def save_as(self, file_name_without_extension):
        file_full_path = self.get_file_full_path(file_name_without_extension)
        App.getDocument(file_name_without_extension).saveAs(file_full_path)

    def save_and_close_active_document(self, file_name_without_extension):
        self.save_as(file_name_without_extension)

        App.closeDocument(file_name_without_extension)
        App.ActiveDocument = None
