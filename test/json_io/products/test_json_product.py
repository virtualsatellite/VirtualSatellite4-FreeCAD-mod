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


App = FreeCAD
Gui = FreeCADGui


class TestJsonProduct(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("Product/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_parse(self):
        json_data = """{
                "name": "BasePlateBottom",
                "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
                "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate",
                "posX": 2.0,
                "posY": 3.0,
                "posZ": 4.0,
                "rotX": 0.1,
                "rotY": 0.2,
                "rotZ": 0.3,
                "children": [
                ]
            }
            """

        json_object = json.loads(json_data)
        json_product = AJsonProduct().parse_from_json(json_object)

        self.assertEqual(json_product.name, "BasePlateBottom", "Property is correctly set")
        self.assertEqual(json_product.uuid, "e8794f3d_86ec_44c5_9618_8b7170c45484", "Property is correctly set")

        self.assertEqual(json_product.part_name, "BasePlate", "Property is correctly set")
        self.assertEqual(json_product.part_uuid, "3d3708fd_5c6c_4af9_b710_d68778466084", "Property is correctly set")

        self.assertEqual(json_product.pos_x, 2000, "Property is correctly set")
        self.assertEqual(json_product.pos_y, 3000, "Property is correctly set")
        self.assertEqual(json_product.pos_z, 4000, "Property is correctly set")

        self.assertEqual(json_product.rot_x, 5.729577951308233, "Property is correctly set")
        self.assertEqual(json_product.rot_y, 11.459155902616466, "Property is correctly set")
        self.assertEqual(json_product.rot_z, 17.188733853924695, "Property is correctly set")
