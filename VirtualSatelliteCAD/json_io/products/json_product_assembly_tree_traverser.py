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
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, JSON_ELEMENT_NAME
from freecad.active_document import ActiveDocument


class JsonProductAssemblyTreeTraverser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def traverse(self, json_object, depth=0, lst_of_depths=[]):
        """
        recursive traverse the tree and create list of depths (length(list) = max_depth):
        containing a list of found assembly (NOT child) nodes at that depth for each depth
        """

        # TODO: change condition?
        if json_object != "":
            print(f"found {json_object[JSON_ELEMENT_NAME]} at {depth}")

            # TODO: test condition
            if(JSON_ELEMNT_CHILDREN in json_object and json_object[JSON_ELEMNT_CHILDREN] != []):
                # only append assemblys that have children
                # print(len(lst_of_depths), depth)
                if(len(lst_of_depths) < depth+1):
                    lst_of_depths.append([])
                    print(f"added depth {depth} to lst_of_depths")
                print(f"found assembly{json_object[JSON_ELEMENT_NAME]} at {depth}")

                lst_of_depths[depth].append(json_object)

                depth += 1

                # recursive call on all children
                for child in json_object[JSON_ELEMNT_CHILDREN]:
                    self.traverse(child, depth)

        return lst_of_depths

    def parse_from_json(self, lst_of_depths, cwd):
        json_product = None

        for depth in reversed(lst_of_depths):
            for assembly in depth:
                json_product = JsonProductAssembly().parse_from_json(assembly)

                # TODO: replace cwd
                active_document = ActiveDocument(cwd).open_set_and_get_document(json_product.get_unique_name())

                # print(assembly)
                # print(json_product)
                json_product.write_to_freecad(active_document)
                active_document.save_as(json_product.get_unique_name())

        return json_product

    def traverse_and_parse_from_json(self, json_object, cwd):
        lst_of_depths = self.traverse(json_object)
        return self.parse_from_json(lst_of_depths, cwd)
