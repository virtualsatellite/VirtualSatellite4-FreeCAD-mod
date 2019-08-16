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
from json_io.parts.json_part import AJsonPart
from test.test_setup import AWorkingDirectoryTest
from freecad.active_document import ActiveDocument
import FreeCAD
import FreeCADGui

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
                "uuidED": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate",
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 0.0,
                "rotX": 0.0,
                "rotY": 0.0,
                "rotZ": 0.0,
                "shape": "BOX",
                "children": [
                ]
            }
            """

        json_object = json.loads(json_data)
        json_part = AJsonPart().parse_from_json(json_object)

        self.assertEqual(json_part.name, "Beam", "Property is correctly set")
        self.assertEqual(json_part.uuid, "6201a731_d703_43f8_ab37_6a0581dfe022", "Property is correctly set")
        self.assertEqual(json_part.shape, "BOX", "Property is correctly set")

        self.assertEqual(json_part.length, 40, "Property is correctly set")
        self.assertEqual(json_part.width,  10, "Property is correctly set")
        self.assertEqual(json_part.height, 300, "Property is correctly set")
        self.assertEqual(json_part.radius, 0, "Property is correctly set and")

        self.assertEqual(json_part.color, 12632256 << 8, "Property is correctly set")

   