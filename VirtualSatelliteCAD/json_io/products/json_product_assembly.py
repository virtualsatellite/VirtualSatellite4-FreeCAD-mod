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

from json_io.products.json_product import AJsonProduct
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, PRODUCT_IDENTIFIER, _get_combined_name_uuid
from json_io.products.json_product_child import JsonProductChild
from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME
from freecad.active_document import ActiveDocument
import FreeCAD
import os

Log = FreeCAD.Console.PrintLog


class JsonProductAssembly(AJsonProduct):
    '''
    This class represents an assembly, which consists of several children
    which basically reference the parts to be imported to this assembly.
    The parts/children contain information about their position and orientation.
    This information is processed to correctly place the parts in the assembly.
    The assembly itself can also have a referenced part. But his one does
    not contain information about its position and rotation. In the current assembly,
    this part is supposed to be imported in the current origin of the assembly.
    In case this assembly is a sub assembly it may have a position and rotation.
    Nevertheless in this particular case, the whole assembly is supposed to be positioned
    and rotated in the super assembly. Actually this assembly is than a child product of
    the super assembly.
    '''

    def _parse_position_and_rotation_from_json(self, json_object):
        '''
        An assembly does not have a position or orientation. If it has these properties
        than it is a sub assembly which has to be processed as a child of the containing
        super assembly.
        '''
        pass

    def parse_from_json(self, json_object):
        '''
        This time the parse method follows the convention
        to not parse the position and orientation. Actually it gets called
        in the super method which refers to the protected method for
        importing position and orientation. This method is overridden in this
        class without implementation. Additionally this method starts parsing
        the children.
        '''
        super().parse_from_json(json_object)

        # Get all children from the json and try to parse them
        # into JsonProductChild objects
        json_object_children = list(json_object[JSON_ELEMNT_CHILDREN])

        self.children = []
        for json_object_child in json_object_children:
            json_product_child = JsonProductChild().parse_from_json(json_object_child)
            # json_product_child.propagate_pos_and_rot_from_parent(self)
            self.children.append(json_product_child)

        # Don't hand back an assembly if there are no children
        if len(self.children) > 0:
            return self
        else:
            return None

    def write_to_freecad(self, active_document):
        # This assembly may refer to a part as well
        # hence if there is a partUuid and if there is a part name, than
        # it should be written to the FreeCAD document as well.
        if self.is_part_reference():
            super().write_to_freecad(active_document)

        # And now write the children, they decide on their own if they reference
        # part or a product
        for child in self.children:
            child.write_to_freecad(active_document)

    def read_from_freecad(self, active_document, working_output_directory):
        """
        Reads an ProductAssembly from FreeCAD
        Then calls read_from_freecad of his children (either another assembly or a ?ProductChild?)
        """
        products_with_sheets = self.get_products_of_active_document(active_document)
        # read the assembly
        # TODO: super().read_from_freecad() and in super read the product and (if available) the corresponding part?
        super().read_from_freecad(active_document, working_output_directory)

        # read the children
        for product, sheet in products_with_sheets:
            name, label = product.Name, product.Label
            # open the document for this child
            # TODO: use source file of a2plus part and then only use the name without fcstd, there probably is a better way to do this
            child_document = ActiveDocument(working_output_directory).open_set_and_get_document(product.sourceFile.split(os.path.sep)[-1][:-6])

            if(PRODUCT_IDENTIFIER in name):
                print(f"Read ProductAssembly '{label}'")
                child = JsonProductAssembly()
            else:
                print(f"Read Product'{label}'")
                # TODO: or JsonProductChild?
                child = AJsonProduct()

            child.read_from_freecad(child_document, working_output_directory)

    def get_products_of_active_document(self, active_document):
        """
        Accesses, sorts and filters objects of the current document.
        NOTE: A document always contains productAssemblies or productChild as long as it is an assembly itself
            Only a document that references one part, thus contains the PART_IDENTIFIER in it's name, references a part
        Returns a list of found products (that have a sheet) and the corresponding sheets
        """
        products, sheets = [], []

        for obj in active_document.app_active_document.Objects:
            name, label = obj.Name, obj.Label
            Log("Object: {}, {}".format(name, label))  # , obj.PropertiesList)

            # TODO: use Labels instead of names if the names contain the identifiers
            if(FREECAD_PART_SHEET_NAME in name):
                sheets.append(obj)
                Log("Object is sheet")
            else:
                products.append(obj)
                Log("Object is product")

        # print([obj.Label for obj in sheets])
        # print([obj.Label for obj in products])

        products_with_sheets = []

        for product in products:
            for sheet in sheets:
                if(product.Label in sheet.Label):
                    products_with_sheets.append((product, sheet))

        print([(p.Label, s.Label) for p, s in products_with_sheets])

        return products_with_sheets

    def get_product_unique_name(self):
        return PRODUCT_IDENTIFIER + _get_combined_name_uuid(self.name, self.uuid)
