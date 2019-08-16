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

import os
import json

from json_io.json_importer import JsonImporter

import FreeCAD
import FreeCADGui
from test.test_setup import AWorkingDirectoryTest
from freecad.active_document import FREECAD_FILE_EXTENSION
from module.environment import Environment
from json_io.json_definitions import JSON_ELEMENT_STL_PATH

App = FreeCAD
Gui = FreeCADGui


# define the name of the directory to be created
TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS = 2


class TestJsonImporter(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("Importer/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

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

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")

        # Check that there is a box with the correct properties
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "40 mm", "Shape has correct size")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Height), "300 mm", "Shape has correct size")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Width), "10 mm", "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Box").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")

    def test_create_part_update_uuid(self):
        '''
        In this test case the uuid is changed. a new uuid has to create a new file.
        '''
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

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")

        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a0666dfe022"
        }"""

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0666dfe022" + FREECAD_FILE_EXTENSION
        App.open(test_file_name)

        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")

    def test_create_part_update_value(self):
        '''
        This test changes an attribute such as the size of the shape.
        Thus the shape is changed but it is still the same object and file.
        '''
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

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "40 mm", "Shape has correct size")

        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.45,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
        }"""

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "450 mm", "Shape has correctly changed size")

    def test_create_part_change_shape(self):
        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a7171dfe022",
            "STL_path": "Test.stl"
        }"""

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)

        # get the current module path and get the directory for the test resource
        # place that path into the json object before executing the transformations
        stl_test_resource_path = Environment.get_test_resource_path("Switch.stl")
        json_object[JSON_ELEMENT_STL_PATH] = stl_test_resource_path

        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a7171dfe022" + FREECAD_FILE_EXTENSION
        App.open(test_file_name)

        # Check that there is the correct object inside
        self.assertIsNotNone(App.ActiveDocument.getObject("Box"), "Got correct object")
        App.closeDocument("Beam_6201a731_d703_43f8_ab37_6a7171dfe022")

        # Now start cyling the objects
        json_object["shape"] = "CYLINDER"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Box"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Cylinder"), "Got correct object")
        App.closeDocument("Beam_6201a731_d703_43f8_ab37_6a7171dfe022")

        # Next object
        json_object["shape"] = "SPHERE"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Cylinder"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Sphere"), "Got correct object")
        App.closeDocument("Beam_6201a731_d703_43f8_ab37_6a7171dfe022")

        # Next object
        json_object["shape"] = "GEOMETRY"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Sphere"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Geometry"), "Got correct object")
        App.closeDocument("Beam_6201a731_d703_43f8_ab37_6a7171dfe022")

        # Next object
        json_object["shape"] = "CONE"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Geometry"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Cone"), "Got correct object")
        App.closeDocument("Beam_6201a731_d703_43f8_ab37_6a7171dfe022")
