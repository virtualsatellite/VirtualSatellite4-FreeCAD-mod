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
from json_io.products.json_product_child import JsonProductChild
from freecad.active_document import ActiveDocument
from json_io.json_definitions import get_product_name_uuid
from test.json_io.test_json_data import TEST_JSON_PRODUCT_WITHOUT_CHILDREN,\
    TEST_JSON_PRODUCT_WITH_ONE_CHILD


App = FreeCAD
Gui = FreeCADGui


class TestJsonProductChild(AWorkingDirectoryTest):

    json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN
    json_data_with_child = TEST_JSON_PRODUCT_WITH_ONE_CHILD

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ProductChild/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_parse(self):
        json_object = json.loads(self.json_data)
        json_product = JsonProductChild().parse_from_json(json_object)

        self.assertEqual(json_product.name, "BasePlateBottom", "Property is correctly set")
        self.assertEqual(json_product.uuid, "e8794f3d_86ec_44c5_9618_8b7170c45484", "Property is correctly set")

        self.assertEqual(json_product.part_name, "BasePlate", "Property is correctly set")
        self.assertEqual(json_product.part_uuid, "3d3708fd_5c6c_4af9_b710_d68778466084", "Property is correctly set")

        # in case the assembly is parsed as a child, like in this test, it has to have positions and orientations
        self.assertEqual(json_product.pos_x, 20, "Property is correctly set")
        self.assertEqual(json_product.pos_y, 30, "Property is correctly set")
        self.assertEqual(json_product.pos_z, 40, "Property is correctly set")

        self.assertAlmostEqual(json_product.rot_x, 20, 5, "Property is correctly set")
        self.assertAlmostEqual(json_product.rot_y, 40, 5, "Property is correctly set")
        self.assertAlmostEqual(json_product.rot_z, 60, 5, "Property is correctly set")

        self.assertFalse(json_product.has_children, "Current product has no children")
        self.assertEquals(json_product.get_part_unique_name(), "BasePlate_3d3708fd_5c6c_4af9_b710_d68778466084", "No children thus references the part")

    def test_parse_with_children(self):
        json_object = json.loads(self.json_data_with_child)
        json_product = JsonProductChild().parse_from_json(json_object)

        self.assertTrue(json_product.has_children, "Current product has children")
        self.assertEquals(json_product.get_part_unique_name(), "BasePlateBottom_e8794f3d_86ec_44c5_9618_8b7170c45484", "No children thus references the part")

    def test_create_part_product_child(self):
        self.create_Test_Part()

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("ProductChild")
        json_object = json.loads(self.json_data)

        json_product = JsonProductChild().parse_from_json(json_object)
        active_document.save_as("ProductChild")

        json_product.write_to_freecad(active_document)

        active_document.save_as("ProductChild")

        # find the object by its label
        product_name = get_product_name_uuid(json_object)
        product_object = active_document.app_active_document.getObjectsByLabel(product_name)[0]

        # check that the euler angles have been applied correctly
        product_placement = product_object.Placement
        euler_angles = product_placement.Rotation.toEuler()
        self.assertAlmostEqualVector(
            euler_angles,
            (60.0, 40.0, 20.0),
            5,
            "Correctly turned the object around its axis"
        )

        # check that the object got moved as expected
        self.assertEqual(product_placement.Base.x, 20, "Property is correctly set")
        self.assertEqual(product_placement.Base.y, 30, "Property is correctly set")
        self.assertEqual(product_placement.Base.z, 40, "Property is correctly set")
