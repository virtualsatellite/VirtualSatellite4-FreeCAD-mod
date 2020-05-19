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


# from freecad.active_document import ActiveDocument
import FreeCAD
from json_io.products.json_product_assembly import JsonProductAssembly
# import json
from json_io.json_definitions import JSON_PARTS, JSON_PRODUCTS
# from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME

Log = FreeCAD.Console.PrintLog


class JsonExporter(object):
    '''
    Provides functionality to export a FreeCAD document into JSON format
    '''

    def __init__(self, working_output_directory):
        self.working_output_directory = working_output_directory

    def full_export(self, active_document):
        """
        Export a FreeCAD document into a JSON file with products and parts
        """

        root_assembly = JsonProductAssembly()

        part_list = []
        # read the root document (this will create the tree and read all children)
        # a list of all found part names and the created part objects will be returned
        Log("Read root assembly...\n")
        root_assembly.read_from_freecad(active_document, self.working_output_directory, part_list)

        Log(part_list)

        Log("Parse root assembly...\n")
        # parse the products using the product assembly tree similar as above
        json_products_dict = root_assembly.parse_to_json(isRoot=True)

        # separate parse the parts into a list
        json_part_list = []
        for _, part in part_list:
            json_part_list.append(part.parse_to_json())

        # create the complete JSON dictionary
        json_dict = {
            JSON_PRODUCTS: json_products_dict,
            JSON_PARTS: json_part_list
        }

        Log(f"Created JSON dictionary: '{json_dict}'\n")

        Log("Export successful\n")

        return json_dict
