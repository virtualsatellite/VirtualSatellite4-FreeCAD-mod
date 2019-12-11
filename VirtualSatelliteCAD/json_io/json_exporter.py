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

    def __init__(self, working_output_directory):
        self.working_output_directory = working_output_directory

    def full_export(self, active_document):

        # parse the root document (this will parse all children
        root_assembly = JsonProductAssembly()
        part_list = []
        root_assembly.read_from_freecad(active_document, self.working_output_directory, part_list)

        print(part_list)
        # for the root assembly we have to provide additional information (name and uuid) here?

        # parse to json
        # TODO: a root assembly does only have name and uuid, so don't parse it like a normal assembly
        # maybe with a dedicated class somehow?
        json_products_dict = root_assembly.parse_to_json(isRoot=True)

        json_part_list = []
        for _, part in part_list:
            json_part_list.append(part.parse_to_json())

        json_dict = {
            JSON_PRODUCTS: json_products_dict,
            JSON_PARTS: json_part_list
        }

        print(json_dict)

        return json_dict
