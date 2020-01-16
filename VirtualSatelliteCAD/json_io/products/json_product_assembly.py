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
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, PRODUCT_IDENTIFIER, PART_IDENTIFIER, \
 _get_combined_name_uuid, JSON_ELEMENT_NAME, JSON_ELEMENT_UUID
from json_io.products.json_product_child import JsonProductChild
from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME
from freecad.active_document import ActiveDocument
from itertools import compress
import FreeCAD
import os
from A2plus.a2p_importpart import updateImportedParts

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
            self.children.append(json_product_child)

        # Don't hand back an assembly if there are no children
        if len(self.children) > 0:
            return self
        else:
            return None

    def parse_to_json(self, isRoot=False):
        if(isRoot):
            json_dict = {
                JSON_ELEMENT_NAME: self.name.replace("_", "-"),
                JSON_ELEMENT_UUID: self.uuid.replace("_", "-")
            }
        else:
            json_dict = super().parse_to_json()

        children_dicts = []
        for child in self.children:

            if(isRoot):
                children_dicts.append(child.parse_to_json())
            else:
                # ignore part of product assembly
                if(not child.get_unique_name() == self.get_unique_name()):
                    children_dicts.append(child.parse_to_json())

        json_dict[JSON_ELEMNT_CHILDREN] = children_dicts

        return json_dict

    def write_to_freecad(self, active_document):
        # This assembly may refer to a part as well
        # hence if there is a partUuid and if there is a part name, than
        # it should be written to the FreeCAD document as well.

        old_products = self.get_products_of_active_document(active_document)
        old_product_names = [o[0].Label for o in old_products]

        # store if a product has to be deleted
        # (because it doesn't exist in the new imported JSON file)
        delete_products = [True] * len(old_product_names)
        update_count = 0

        if self.is_part_reference():
            name = _get_combined_name_uuid(self.part_name, self.part_uuid)
            if(name in old_product_names):
                # update
                update_count += 1
                super().write_to_freecad(active_document, create=False)
                delete_products[old_product_names.index(name)] = False
            else:
                # create
                super().write_to_freecad(active_document)

        # And now write the children, they decide on their own if they reference
        # part or a product
        for child in self.children:
            name = child.get_unique_name()
            if(name in old_product_names):
                # update
                update_count += 1
                child.write_to_freecad(active_document, create=False)
                delete_products[old_product_names.index(name)] = False
            else:
                # create
                child.write_to_freecad(active_document)

        # delete remaining old products
        old_products = list(compress(old_products, delete_products))
        for old_product in old_products:
            active_document.app_active_document.removeObject(old_product[0].Name)
            active_document.app_active_document.removeObject(old_product[1].Name)

        # only if there were updates instead of creates
        if(update_count > 0):
            # update already read in parts
            updateImportedParts(active_document.app_active_document)

    def read_from_freecad(self, active_document, working_output_directory, part_list, freecad_object=None, freecad_sheet=None):
        """
        Reads an ProductAssembly from FreeCAD
        Then calls read_from_freecad of his children (either another assembly or a ProductChild)
        """
        products_with_sheets = self.get_products_of_active_document(active_document)
        # read the assembly
        super().read_from_freecad(active_document, working_output_directory, part_list, freecad_object, freecad_sheet)

        self.children = []
        # read the children
        for product, sheet in products_with_sheets:
            name, label = product.Name, product.Label
            # use the source file of a2plus part
            # then get the file name (.split(os.path.sep)[-1]) and ignore the FreeCAD file ending ([:-6])
            child_file_name = product.sourceFile.split(os.path.sep)[-1][:-6]

            # open the document for this child
            child_document = ActiveDocument(working_output_directory).open_set_and_get_document(child_file_name)

            if(PRODUCT_IDENTIFIER in name):
                Log(f"Read ProductAssembly '{label}'\n")
                child = JsonProductAssembly()
            else:
                Log(f"Read Product '{label}'\n")
                child = AJsonProduct()

            child.read_from_freecad(child_document, working_output_directory, part_list, freecad_object=product, freecad_sheet=sheet)
            child_document.close_active_document(child_file_name)

            self.children.append(child)

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
            Log("Object: {}, {}\n".format(name, label))

            if(FREECAD_PART_SHEET_NAME in name):
                sheets.append(obj)
                Log("Object is sheet\n")
            elif(PRODUCT_IDENTIFIER in name or PART_IDENTIFIER in name):
                products.append(obj)
                Log("Object is product\n")

        products_with_sheets = []

        for product in products:
            for sheet in sheets:
                if(product.Label in sheet.Label):
                    products_with_sheets.append((product, sheet))

        Log(f"Found products with sheets: '{[(p.Label, s.Label) for p, s in products_with_sheets]}'\n")

        return products_with_sheets

    def get_product_unique_name(self):
        return PRODUCT_IDENTIFIER + _get_combined_name_uuid(self.name, self.uuid)
