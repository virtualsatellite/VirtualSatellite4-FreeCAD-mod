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
from test.json_io.test_json_data import TEST_JSON_PART_BOX
from json_io.json_definitions import PART_IDENTIFIER

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
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_part = AJsonPart().parse_from_json(json_object)

        self.assertEqual(json_part.name, "Beam", "Property is correctly set")
        self.assertEqual(json_part.uuid, "6201a731-d703-43f8-ab37-6a0581dfe022", "Property is correctly set")
        self.assertEqual(json_part.shape, "BOX", "Property is correctly set")

        self.assertEqual(json_part.length, 40, "Property is correctly set")
        self.assertEqual(json_part.width,  20, "Property is correctly set")
        self.assertEqual(json_part.height, 10, "Property is correctly set")
        self.assertEqual(json_part.radius, 0, "Property is correctly set and")

        self.assertEqual(json_part.color, 12632256 << 8, "Property is correctly set")

    def test_create_part(self):
        json_data = TEST_JSON_PART_BOX

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Write")
        json_object = json.loads(json_data)

        json_part = AJsonPart()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        self.assertIsNotNone(App.ActiveDocument.getObject("Box"), "The Box object got created")
        self.assertEquals(Gui.ActiveDocument.getObject("Box").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")

    def test_create_and_read_part(self):
        json_data = TEST_JSON_PART_BOX

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Write")
        json_object = json.loads(json_data)

        json_part = AJsonPart()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        read_part = AJsonPart()
        freecad_object = active_document.app_active_document.Objects[0]
        freecad_sheet = active_document.app_active_document.Objects[1]

        read_part.read_from_freecad(freecad_object, freecad_sheet)
        read_json = read_part.parse_to_json()

        self.assertJsonObjectsEqual(json_object, read_json, "Equal JSON objects")

    def test_get_part_unique_name(self):
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)

        json_part = AJsonPart()
        json_part.parse_from_json(json_object)

        self.assertEquals(json_part.get_unique_name(), PART_IDENTIFIER + "Beam_6201a731___d703___43f8___ab37___6a0581dfe022", "Correct unique name")
