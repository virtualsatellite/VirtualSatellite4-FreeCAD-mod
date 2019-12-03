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

from json_io.products.json_product_assembly import JsonProductAssembly
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, JSON_ELEMENT_NAME, PRODUCT_IDENTIFIER
from freecad.active_document import ActiveDocument
import FreeCAD
Log = FreeCAD.Console.PrintLog


class JsonProductAssemblyTreeTraverser(object):
    '''
    This class provides functionality to traverse a product tree to parse the product assemblies in the right order
    '''

    def __init__(self, working_output_directory):
        self._lst_of_depths = []
        self.working_output_directory = working_output_directory

    def traverse(self, json_object, depth=0):
        """
        Recursive traverse the tree and create a list containing the found depths,
        that for each depth contains a list of found assembly (NOT child) nodes at that depth
        """

        # only look for products that have children
        if(JSON_ELEMNT_CHILDREN in json_object and json_object[JSON_ELEMNT_CHILDREN] != []):

            # if the current depth has no list in the _lst_of_depths, add it
            if(len(self._lst_of_depths) < depth + 1):
                self._lst_of_depths.append([])
                Log(f"Added depth {depth} to _lst_of_depths\n")

            # append found assembly to the list
            self._lst_of_depths[depth].append(json_object)
            Log(f"Found assembly '{json_object[JSON_ELEMENT_NAME]}' at {depth}\n")

            # recursive call on all children
            for child in json_object[JSON_ELEMNT_CHILDREN]:
                self.traverse(child, depth+1)

    def parse_from_json(self):
        """
        Iterate through the list created by traversing the tree in reverse and parse the found product assemblies
        """
        json_product, active_document = None, None

        # parse in reverse order
        for depth in reversed(self._lst_of_depths):
            for assembly in depth:
                Log(f"Parsing '{assembly[JSON_ELEMENT_NAME]}'\n")

                json_product = JsonProductAssembly().parse_from_json(assembly)
                active_document = ActiveDocument(self.working_output_directory).open_set_and_get_document(json_product.get_product_unique_name())
                json_product.write_to_freecad(active_document)
                active_document.save_and_close_active_document(json_product.get_product_unique_name())

        # the last json_product is the root of the assembly, open it again for the UI
        if(json_product is not None):
            active_document = ActiveDocument(self.working_output_directory).open_set_and_get_document(json_product.get_unique_name())

        return json_product, active_document

    def traverse_and_parse_from_json(self, json_object):
        self.traverse(json_object)
        return self.parse_from_json()
