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


class TestJsonPart(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("Part/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_parse(self):
        json_data = """{
            "name": "Beam",
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
            "shape": "BOX",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "color": 12632256
        }"""

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

    def test_create_part(self):
        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
        }"""

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Write")
        json_object = json.loads(json_data)

        json_part = AJsonPart()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        self.assertIsNotNone(App.ActiveDocument.getObject("Box"), "The Box object got created")
        self.assertEquals(Gui.ActiveDocument.getObject("Box").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")
