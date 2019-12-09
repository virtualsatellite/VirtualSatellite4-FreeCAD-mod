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
from json_io.json_definitions import PART_IDENTIFIER, PRODUCT_IDENTIFIER, SHEET_IDENTIFIER

Log = FreeCAD.Console.PrintLog


class JsonExporter(object):

    def __init__(self):
        pass

    def get_objects_of_active_document(self):
        """
        Accesses, sorts and filters objects of the current document.
        Returns a list of found:
            - products (that have a sheet)
            - parts (that have a sheet)
            - sheets
        """
        products, parts, sheets = [], [], []

        for obj in FreeCAD.ActiveDocument.Objects:
            name, label = obj.Name, obj.Label
            Log("Object: {}, {}".format(name, label))  # , obj.PropertiesList)

            # TODO: use Labels instead of names if the names contain the identifiers
            if(SHEET_IDENTIFIER in name):
                sheets.append(obj)
                Log("Object is sheet")
            else:
                if(PART_IDENTIFIER in name):
                    parts.append(obj)
                    Log("Object is part")
                elif(PRODUCT_IDENTIFIER in name):
                    products.append(obj)
                    Log("Object is product")

            def is_in_sheets(obj):
                return any(obj.Label in sheet.Label for sheet in sheets)

            filtered_parts = list(filter(lambda part: is_in_sheets(part), parts))
            filtered_products = list(filter(lambda product: is_in_sheets(product), products))

            print([obj.Label for obj in sheets])
            print([obj.Label for obj in filtered_parts])
            print([obj.Label for obj in filtered_products])

        return filtered_products, filtered_parts, sheets

    def parse_freecad_parts_to_json(self, parts, products, sheets, json_parts):
        for part in parts:
            print(part.Label, part.Shape)

    def full_export(self):  # , active_document):

        # read the root document
        root_products, root_parts, root_sheets = self.get_objects_of_active_document()

        json_parts = []
        # parse the parts to json
        self.parse_freecad_parts_to_json(root_parts, root_products, root_sheets, json_parts)

        return "test string"
