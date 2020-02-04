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
from json_io.products.json_product import AJsonProduct
from test.json_io.test_json_data import TEST_JSON_PRODUCT_WITHOUT_CHILDREN, TEST_JSON_PRODUCT_WITHOUT_CHILDREN_WITHOUT_PART
from json_io.json_definitions import PART_IDENTIFIER, \
    JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z
from freecad.active_document import ActiveDocument

App = FreeCAD
Gui = FreeCADGui


class TestJsonProduct(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("Product/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_parse_from_json(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        self.assertEqual(json_product.name, "BasePlateBottom", "Property is correctly set")
        self.assertEqual(json_product.uuid, "e8794f3d_86ec_44c5_9618_8b7170c45484", "Property is correctly set")

        self.assertEqual(json_product.part_name, "BasePlate", "Property is correctly set")
        self.assertEqual(json_product.part_uuid, "3d3708fd_5c6c_4af9_b710_d68778466084", "Property is correctly set")

        self.assertEqual(json_product.pos_x, 20, "Property is correctly set")
        self.assertEqual(json_product.pos_y, 30, "Property is correctly set")
        self.assertEqual(json_product.pos_z, 40, "Property is correctly set")

        self.assertAlmostEqual(json_product.rot_x, 20, 5, "Property is correctly set")
        self.assertAlmostEqual(json_product.rot_y, 40, 5, "Property is correctly set")
        self.assertAlmostEqual(json_product.rot_z, 60, 5, "Property is correctly set")

        self.assertFalse(json_product.has_children, "The defined product has an empty list of children")

    def test_parse_to_json(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        read_json = json_product.parse_to_json()

        self.assertJsonObjectsEqual(json_object, read_json, "Equal JSON objects")

    def test_get_unique_names(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        self.assertEquals(json_product.get_unique_name(), "BasePlateBottom_e8794f3d_86ec_44c5_9618_8b7170c45484", "Correct unique name")
        self.assertEquals(json_product.get_part_unique_name(), PART_IDENTIFIER + "BasePlate_3d3708fd_5c6c_4af9_b710_d68778466084", "Correct unique name")

    def test_is_part_reference(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN_WITHOUT_PART

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        self.assertFalse(json_product.is_part_reference(), "The current product does not reference a part")

        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        self.assertTrue(json_product.is_part_reference(), "The current product references a part")

    def test_rotation(self):
        self.create_Test_Part()

        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)
        rot_old = [json_product.rot_x, json_product.rot_y, json_product.rot_z]

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("Rotation_test")
        json_product.write_to_freecad(active_document)
        freecad_object = active_document.app_active_document.Objects[0]

        json_product._get_freecad_rotation(freecad_object)

        read_json = json_product.parse_to_json()

        self.assertAlmostEqualVector(rot_old, [json_product.rot_x, json_product.rot_y, json_product.rot_z], msg="Product rotations are equal")
        self.assertAlmostEqualVector([json_object[JSON_ELEMENT_ROT_X], json_object[JSON_ELEMENT_ROT_Y], json_object[JSON_ELEMENT_ROT_Z]],
                                     [read_json[JSON_ELEMENT_ROT_X], read_json[JSON_ELEMENT_ROT_Y], read_json[JSON_ELEMENT_ROT_Z]],
                                     msg="Rotations in JSON files are equal")
