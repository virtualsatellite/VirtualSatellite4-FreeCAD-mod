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
from freecad.active_document import ActiveDocument
import FreeCAD
import FreeCADGui
from json_io.parts.json_part_sphere import JsonPartSphere
from test.json_io.test_json_data import TEST_JSON_PART_SPHERE
from json_io.json_definitions import JSON_ELEMENT_RADIUS

App = FreeCAD
Gui = FreeCADGui


class TestJsonPartSphere(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartSphere/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_create_part_sphere(self):
        json_data = TEST_JSON_PART_SPHERE

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSphere")
        json_object = json.loads(json_data)

        json_part = JsonPartSphere()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        active_document.save_as("PartSphere")

        self.assertIsNotNone(App.ActiveDocument.getObject("Sphere"), "The Sphere object got created")

        # Check that there is a box with the correct properties
        self.assertEquals(App.ActiveDocument.getObject("Sphere").Radius, 3, "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Sphere").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")

    def test_create_and_read_part_sphere(self):
        json_data = TEST_JSON_PART_SPHERE

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSphere")
        json_object = json.loads(json_data)

        json_part = JsonPartSphere()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        read_part = JsonPartSphere()
        freecad_object = active_document.app_active_document.Objects[0]
        freecad_sheet = active_document.app_active_document.Objects[1]

        read_part.read_from_freecad(freecad_object, freecad_sheet)
        read_json = read_part.parse_to_json()

        self.assertJsonObjectsEqual(json_object, read_json, "Equal JSON objects")

    def test_create_change_and_read_part_sphere(self):
        json_data = TEST_JSON_PART_SPHERE

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSphere")
        json_object = json.loads(json_data)

        json_part = JsonPartSphere()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        read_part = JsonPartSphere()
        freecad_object = active_document.app_active_document.Objects[0]
        freecad_sheet = active_document.app_active_document.Objects[1]

        # Change sphere properties
        freecad_object.Radius = 10

        read_part.read_from_freecad(freecad_object, freecad_sheet)
        read_json = read_part.parse_to_json()

        # check that only the expected values got changed
        self.assertJsonObjectsAlmostEqual(
            read_json, json_object, [JSON_ELEMENT_RADIUS],
            "JSON objects at most differ in radius")

        # check that the values got changed correct
        self.assertEqual(read_json[JSON_ELEMENT_RADIUS], 0.01, "Radius set correct")
