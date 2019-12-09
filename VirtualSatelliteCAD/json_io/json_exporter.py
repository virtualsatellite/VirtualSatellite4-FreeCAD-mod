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
# from json_io.json_definitions import PART_IDENTIFIER, PRODUCT_IDENTIFIER
# from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME

Log = FreeCAD.Console.PrintLog


class JsonExporter(object):

    def __init__(self, working_output_directory):
        self.working_output_directory = working_output_directory

#     def get_products_of_active_document(self):
#         """
#         Accesses, sorts and filters objects of the current document.
#         NOTE: A document always contains productAssemblies or productChild as long as it is an assemly itself
#             Only a document that references one part, thus contains the PART_IDENTIFIER in it's name, references a part
#         Returns a list of found:
#             - products (that have a sheet) and the corresponding sheets
#         """
#         products, sheets = [], []
#
#         for obj in FreeCAD.ActiveDocument.Objects:
#             name, label = obj.Name, obj.Label
#             Log("Object: {}, {}".format(name, label))  # , obj.PropertiesList)
#
#             # TODO: use Labels instead of names if the names contain the identifiers
#             if(FREECAD_PART_SHEET_NAME in name):
#                 sheets.append(obj)
#                 Log("Object is sheet")
#             else:
#                 products.append(obj)
#                 Log("Object is product")
#
#         print([obj.Label for obj in sheets])
#         print([obj.Label for obj in products])
#
#         products_with_sheets = []
#
#         for product in products:
#             for sheet in sheets:
#                 if(product.Label in sheet.Label):
#                     products_with_sheets.append((product, sheet))
#
#         print([(p.Label, s.Label) for p, s in products_with_sheets])
#
#         return products_with_sheets

#     def parse_freecad_parts_to_json(self, parts, products, sheets, json_parts):
#         print(parts[0].PropertiesList)
#         for part in parts:
#             print(part.Label, part.Shape)

    def full_export(self, active_document):

        # parse the root document (this will parse all children
        root_assembly = JsonProductAssembly()
        root_assembly.read_from_freecad(active_document, self.working_output_directory)

        return "test string"
