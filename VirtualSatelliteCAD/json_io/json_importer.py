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
from freecad.active_document import ActiveDocument
from json_io.parts.json_part_factory import JsonPartFactory
from json_io.products.json_product_assembly_tree_traverser import JsonProductAssemblyTreeTraverser
from json_io.json_definitions import get_part_name_uuid, JSON_PRODUCTS, JSON_PARTS, PART_IDENTIFIER

App = FreeCAD
Gui = FreeCADGui
Log = FreeCAD.Console.PrintLog
Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Wrn = FreeCAD.Console.PrintWarning


class JsonImporter(object):
    '''
    Provides functionality to import a JSON created by Virtual Satellite into FreeCAD
    '''

    def __init__(self, working_output_directory):
        self.working_output_directory = working_output_directory

    def create_or_update_part(self, json_object):
        Log("Creating or Updating a part...\n")
        json_part = JsonPartFactory().create_from_json(json_object)

        part_file_name = ""

        if json_part is not None:
            # Use the name to create the part document
            # should be careful in case the name already exists.
            # thus it is combined with the uuid. not really nice
            # but definitely efficient
            part_file_name = PART_IDENTIFIER + get_part_name_uuid(json_object)

            active_document = ActiveDocument(self.working_output_directory).open_set_and_get_document(part_file_name)

            json_part.write_to_freecad(active_document)

            active_document.save_and_close_active_document(part_file_name)
            Log("Saved part to file: " + part_file_name + "\n")
        else:
            Log("Visualization shape is most likely NONE, therefore no file is created\n")

        return part_file_name

    def full_import(self, json_object):
        '''
        Import a whole json file's products and parts into a FreeCAD document
        '''
        Log(f"Calling the importer'\n")

        json_parts = json_object[JSON_PARTS]

        part_file_names = []
        for part in json_parts:
            part_file_names.append(self.create_or_update_part(part))

        traverser = JsonProductAssemblyTreeTraverser(self.working_output_directory, part_file_names)
        json_product, active_document = traverser.traverse_and_parse_from_json(json_object[JSON_PRODUCTS])

        Log(f"Import successful\n")

        return part_file_names, json_product, active_document
