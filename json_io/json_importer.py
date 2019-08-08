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
from json_io.json_part import JsonPart
from json_io.json_definitions import FREECAD_FILE_EXTENSION
import FreeCADGui
import os

App = FreeCAD
Gui = FreeCADGui
Log = FreeCAD.Console.PrintLog
Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Wrn = FreeCAD.Console.PrintWarning


class JsonImporter(object):
    '''
    classdocs
    '''

    def __init__(self, working_ouput_directory):
        self.working_output_directory = working_ouput_directory

    def create_or_update_part(self, json_object):
        Log('Creating or Updating a part...\n')
        json_part = JsonPart().parse(json_object)

        # Use the name to create the part document
        # should be careful in case the name already exists.
        # thus it is combined with the uuid. not really nice
        # but definitely efficient
        part_file_name = str(json_part.name + "_" + json_part.uuid)
        part_file_fullpath = self.working_output_directory + part_file_name + FREECAD_FILE_EXTENSION

        if(os.path.isfile(part_file_fullpath)):
            Log('Open exisitng part file for update...\n')
            documents = list(App.listDocuments().keys())
            # If the document is not yet laoded, open it
            if documents.count(part_file_name) == 0:
                App.open(part_file_fullpath)
        else:
            Log('Create new part file...\n')
            App.newDocument(part_file_name)

        App.setActiveDocument(part_file_name)
        App.ActiveDocument = App.getDocument(part_file_name)

        part_file_fullpath = self.working_output_directory + part_file_name + FREECAD_FILE_EXTENSION

        # Dispatch to creation method depending on shape type
        create_or_update_method_name = "create_or_update_" + json_part.shape.lower()
        create_or_update_dispatch = getattr(self, create_or_update_method_name, lambda: "Invalid call to : " + create_or_update_method_name)
        create_or_update_dispatch(json_part)

        self.create_or_update_sheet(json_part)

        App.getDocument(part_file_name).saveAs(part_file_fullpath)
        App.closeDocument(part_file_name)
        Log('Saved part to file: ' + part_file_fullpath + "\n")

    def create_or_update_sheet(self, json_part):
        sheet = App.ActiveDocument.getObject("VirtualSatellite")
        if sheet is None:
            sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "VirtualSatellite")

        sheet.set("A1", "Virtual Satellite Part Data")
        sheet.set("A2", "Name")
        sheet.set("B2", "Value")
        sheet.set("C2", "Unit")
        sheet.setStyle("A1:C2", "bold")

        sheet_line = 3
        for json_part_attribute_name in list(json_part.attributes.keys()):

            json_part_attribute_value = str(getattr(json_part, json_part_attribute_name))
            json_part_attribute_unit = json_part.attributes[json_part_attribute_name]

            sheet.set("A" + str(sheet_line), json_part_attribute_name)
            sheet.set("B" + str(sheet_line), json_part_attribute_value)
            sheet.set("C" + str(sheet_line), json_part_attribute_unit)

            sheet_line += 1

    def read_from_sheet(self, attribute_name):
        sheet = App.ActiveDocument.getObject("VirtualSatellite")
        column_a_cells = list(filter(lambda x: x.startswith('A'), sheet.PropertiesList))

        for a_cell in column_a_cells:
            if a_cell == attribute_name:
                b_cell = a_cell.replace("A", "B")
                return sheet.get(b_cell)

    def create_or_update_box(self, json_part):
        if App.ActiveDocument.getObject('Box') is None:
            App.ActiveDocument.addObject("Part::Box", "Box")

        App.ActiveDocument.getObject("Box").Label = json_part.name

        App.ActiveDocument.getObject("Box").Length = json_part.length_x + ' m'
        App.ActiveDocument.getObject("Box").Height = json_part.length_y + ' m'
        App.ActiveDocument.getObject("Box").Width = json_part.length_z + ' m'

        Gui.ActiveDocument.getObject("Box").ShapeColor = json_part.color

        App.ActiveDocument.recompute()

    def create_or_update_cone(self, json_part):
        pass

    def create_or_update_cylinder(self, json_part):
        pass

    def create_or_update_sphere(self, json_part):
        pass

    def create_or_update_geometry(self, json_part):
        pass
