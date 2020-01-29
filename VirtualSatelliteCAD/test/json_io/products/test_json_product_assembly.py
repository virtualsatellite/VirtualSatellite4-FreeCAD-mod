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


import json
from test.test_setup import AWorkingDirectoryTest
import FreeCAD
import FreeCADGui
from json_io.products.json_product_assembly import JsonProductAssembly
from freecad.active_document import ActiveDocument
from test.json_io.test_json_data import TEST_JSON_PRODUCT_WITH_CHILDREN,\
    TEST_JSON_PRODUCT_WITHOUT_CHILDREN, TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD,\
    TEST_JSON_PRODUCT_ROOT
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, PRODUCT_IDENTIFIER, \
    JSON_ELEMENT_POS_X, JSON_ELEMENT_POS_Y, JSON_ELEMENT_POS_Z, \
    JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z
from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME
from json_io.products.json_product_assembly_tree_traverser import JsonProductAssemblyTreeTraverser

App = FreeCAD
Gui = FreeCADGui


class TestJsonProductAssembly(AWorkingDirectoryTest):

    json_data = TEST_JSON_PRODUCT_WITH_CHILDREN

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ProductAssembly/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_parse_from_json_with_children(self):
        json_object = json.loads(self.json_data)
        json_product = JsonProductAssembly().parse_from_json(json_object)

        self.assertEqual(json_product.name, "BasePlateBottom1", "Property is correctly set")
        self.assertEqual(json_product.uuid, "e8794f3d_86ec_44c5_9618_8b7170c45484", "Property is correctly set")

        self.assertEqual(json_product.part_name, "BasePlate", "Property is correctly set")
        self.assertEqual(json_product.part_uuid, "3d3708fd_5c6c_4af9_b710_d68778466084", "Property is correctly set")

        # Properties have to be 0 since an assembly itself has no position and orientation
        self.assertEqual(json_product.pos_x, 0, "Property is correctly set")
        self.assertEqual(json_product.pos_y, 0, "Property is correctly set")
        self.assertEqual(json_product.pos_z, 0, "Property is correctly set")

        self.assertEqual(json_product.rot_x, 0.0, "Property is correctly set")
        self.assertEqual(json_product.rot_y, 0.0, "Property is correctly set")
        self.assertEqual(json_product.rot_z, 0.0, "Property is correctly set")

        # Now check for the children
        self.assertEquals(len(json_product.children), 2, "Parsed two children")

        json_product_child_1 = json_product.children[0]
        json_product_child_2 = json_product.children[1]

        self.assertEqual(json_product_child_1.name, "BasePlateBottom2", "Parsed correct child")
        self.assertEqual(json_product_child_2.name, "BasePlateTop", "Parsed correct child")

        # Check that position and rotation from parent are propagated correctly
        self.assertEqual(json_product_child_1.pos_x, 0, "Property is correctly set")
        self.assertEqual(json_product_child_1.pos_y, 0, "Property is correctly set")
        self.assertEqual(json_product_child_1.pos_z, 0, "Property is correctly set")

        self.assertEqual(json_product_child_1.rot_x, 0.0, "Property is correctly set")
        self.assertEqual(json_product_child_1.rot_y, 0.0, "Property is correctly set")
        self.assertEqual(json_product_child_1.rot_z, 0.0, "Property is correctly set")

        self.assertEqual(json_product_child_2.pos_x, 0, "Property is correctly set")
        self.assertEqual(json_product_child_2.pos_y, 0, "Property is correctly set")
        self.assertEqual(json_product_child_2.pos_z, 500.0, "Property is correctly set")

        self.assertEqual(json_product_child_2.rot_x, 0.0, "Property is correctly set")
        self.assertEqual(json_product_child_2.rot_y, 0.0, "Property is correctly set")
        self.assertEqual(json_product_child_2.rot_z, 0.0, "Property is correctly set")

    def test_parse_from_json_with_no_children(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = JsonProductAssembly().parse_from_json(json_object)

        self.assertIsNone(json_product, "There is no assembly if there are no children")

    def test_parse_to_json(self):
        json_object = json.loads(self.json_data)
        json_product = JsonProductAssembly().parse_from_json(json_object)

        read_json = json_product.parse_to_json()

        # positions and rotations of root assembly won't be parsed
        diff = [JSON_ELEMENT_POS_X, JSON_ELEMENT_POS_Y, JSON_ELEMENT_POS_Z,
                JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z]

        self.assertJsonObjectsAlmostEqual(json_object, read_json, diff, "Equal JSON objects")

    def test_create_part_product_assembly_with_root_part(self):
        self.create_Test_Part()

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("ProductAssemblyRootPart")
        json_object = json.loads(self.json_data)
        json_product = JsonProductAssembly().parse_from_json(json_object)

        json_product.write_to_freecad(active_document)

        active_document.save_as("ProductAssemblyRootPart")

        # find the object by its label there should be three objects identifiable in the current export
        # the part in the product and two times the referenced parts in the children.
        self.assertEquals(len(json_product.children), 2, "correct amount of children")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 6, "Found correct amount of root objects 3 objects plus 3 sheets")

        product_part_name = json_product.get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_part_name)[0]
        self.assertIsNotNone(product_object, "Found an object under the given part name")

        product_child1_part_name = json_product.children[0].get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_child1_part_name)[0]
        self.assertIsNotNone(product_object, "Found an object under the given part name")

        product_child2_part_name = json_product.children[1].get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_child2_part_name)[0]
        self.assertIsNotNone(product_object, "Found an object under the given part name")

    def test_create_part_product_subassembly_with_root_part(self):
        json_data = TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD
        self.create_Test_Part()

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("ProductSubassemblyRootPart")

        json_object = json.loads(json_data)

        subassembly = json_object[JSON_ELEMNT_CHILDREN][0]
        json_product = JsonProductAssembly().parse_from_json(subassembly)

        json_product.write_to_freecad(active_document)
        active_document.save_as("ProductSubassemblyRootPart")

        self.assertEquals(len(json_product.children), 1, "correct amount of children")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 4, "Found correct amount of root objects 2 objects plus 2 sheets")

        product_part_name = json_product.get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_part_name)[0]
        self.assertIsNotNone(product_object, "Found an object under the given part name")

        product_child1_part_name = json_product.children[0].get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_child1_part_name)[0]
        self.assertIsNotNone(product_object, "Found an object under the given part name")

    def test_create_part_product_assembly_and_subassembly_with_root_part_manual(self):
        json_data = TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD
        self.create_Test_Part()

        json_object = json.loads(json_data)

        subassembly = json_object[JSON_ELEMNT_CHILDREN][0]

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
            PRODUCT_IDENTIFIER + "BasePlateBottom2_e8794f3d_86ec_44c5_9618_8b7170c45484")

        json_product = JsonProductAssembly().parse_from_json(subassembly)
        json_product.write_to_freecad(active_document)
        active_document.save_as(PRODUCT_IDENTIFIER + "BasePlateBottom2_e8794f3d_86ec_44c5_9618_8b7170c45484")

        self.assertEquals(len(active_document.app_active_document.RootObjects), 4, "Found correct amount of root objects 2 objects plus 2 sheets")

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("ProductAssemblyAndSubassemblyRootPart")

        json_product = JsonProductAssembly().parse_from_json(json_object)
        json_product.write_to_freecad(active_document)
        active_document.save_as("ProductAssemblyAndSubassemblyRootPart")

        self.assertEquals(len(active_document.app_active_document.RootObjects), 6, "Found correct amount of root objects 3 objects plus 3 sheets")

    def test_get_products_of_active_document(self):
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("ProductAssemblyActiveDocuments")
        json_object = json.loads(self.json_data)
        json_product = JsonProductAssembly().parse_from_json(json_object)

        json_product.write_to_freecad(active_document)

        products = JsonProductAssembly().get_products_of_active_document(active_document)

        self.assertEqual(len(products), 3, "Found correct number of 3 products")

        self.assertEqual(products[0][0].Label, "BasePlateBottom1_e8794f3d_86ec_44c5_9618_8b7170c45484", "Found correct product")
        self.assertEqual(products[0][1].Label, FREECAD_PART_SHEET_NAME + "_" + "BasePlateBottom1_e8794f3d_86ec_44c5_9618_8b7170c45484", "Found correct sheet")
        self.assertEqual(products[1][0].Label, "BasePlateBottom2_e8794f3d_86ec_44c5_9618_8b7170c45484", "Found correct product")
        self.assertEqual(products[1][1].Label, FREECAD_PART_SHEET_NAME + "_" + "BasePlateBottom2_e8794f3d_86ec_44c5_9618_8b7170c45484", "Found correct sheet")
        self.assertEqual(products[2][0].Label, "BasePlateTop_a199e3bd_3bc1_426d_8321_e9bd829339b3", "Found correct product")
        self.assertEqual(products[2][1].Label, FREECAD_PART_SHEET_NAME + "_" + "BasePlateTop_a199e3bd_3bc1_426d_8321_e9bd829339b3", "Found correct sheet")

    def test_read_from_freecad(self):
        self.create_Test_Part()

        json_object = json.loads(TEST_JSON_PRODUCT_ROOT)
        traverser = JsonProductAssemblyTreeTraverser(self._WORKING_DIRECTORY)
        json_product, active_document = traverser.traverse_and_parse_from_json(json_object)

        json_product.write_to_freecad(active_document)

        part_list = []
        root_assembly = JsonProductAssembly()

        root_assembly.read_from_freecad(active_document, self._WORKING_DIRECTORY, part_list)

        self.assertEqual(len(part_list), 1, "Found correct number of 1 part")
        self.assertEqual(part_list[0][0], "part_BasePlate_3d3708fd_5c6c_4af9_b710_d68778466084", "Found correct part")

        json_products_dict = root_assembly.parse_to_json(isRoot=True)

        self.assertJsonObjectsAlmostEqual(json_products_dict, json_object, msg="Found equal dictionaries (except rotation floats)",
                                          static_keys=[JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z])
