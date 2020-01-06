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
from json_io.parts.json_part_geometry import JsonPartGeometry
from module.environment import Environment
from json_io.json_definitions import JSON_ELEMENT_STL_PATH
from test.json_io.test_json_data import TEST_JSON_PART_GEOMETRY
from shutil import copyfile
import os

App = FreeCAD
Gui = FreeCADGui


class TestJsonPartGeometry(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartGeometry/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_create_part_geometry(self):
        json_data = TEST_JSON_PART_GEOMETRY

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartGeometry")
        json_object = json.loads(json_data)

        # get the current module path and get the directory for the test resource
        # place that path into the json object before executing the transformations
        stl_test_resource_path = Environment.get_test_resource_path("Switch.stl")
        json_object[JSON_ELEMENT_STL_PATH] = stl_test_resource_path

        json_part = JsonPartGeometry()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        active_document.save_as("PartGeometry")

        self.assertIsNotNone(App.ActiveDocument.getObject("Geometry"), "The Box object got created")

        # Check that the extra attribute for the STL files got written to the sheet
        sheet_stl_path = json_part.sheet.read_sheet_attribute(active_document, "stl_path")
        self.assertEqual(sheet_stl_path, stl_test_resource_path, "The path is perfectly written to the spreadsheet")

        # Check that there is a box with the correct properties
        self.assertEquals(Gui.ActiveDocument.getObject("Geometry").ShapeColor,
                          (0.003921568859368563, 0.007843137718737125, 0.9098039269447327, 0.0),
                          "Shape has correct color")

    def test_create_and_read_part_geometry(self):
        json_data = TEST_JSON_PART_GEOMETRY

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartGeometry")
        json_object = json.loads(json_data)

        # get the current module path and get the directory for the test resource
        # place that path into the json object before executing the transformations
        stl_test_resource_path = Environment.get_test_resource_path("Switch.stl")
        stl_test_resource_path_cp = os.path.join(self._WORKING_DIRECTORY, "Switch_cp.stl")
        copyfile(stl_test_resource_path, stl_test_resource_path_cp)
        json_object[JSON_ELEMENT_STL_PATH] = stl_test_resource_path_cp

        json_part = JsonPartGeometry()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        read_part = JsonPartGeometry()
        # first 3 objects belong to the stl
        freecad_object = active_document.app_active_document.Objects[3]
        freecad_sheet = active_document.app_active_document.Objects[4]

        read_part.read_from_freecad(freecad_object, freecad_sheet)
        read_json = read_part.parse_to_json()

        self.assertJsonObjectsEqual(json_object, read_json, "Equal JSON objects")
