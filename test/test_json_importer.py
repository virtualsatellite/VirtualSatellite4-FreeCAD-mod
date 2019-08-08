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

import unittest

import os
import json

from json_io.json_importer import JsonImporter
from json_io.json_definitions import FREECAD_FILE_EXTENSION

import FreeCAD
import FreeCADGui

App = FreeCAD
Gui = FreeCADGui


# define the name of the directory to be created
TEST_WORKING_DIRECTORY = "/tmp/FreeCADtest/"
TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS = 2


class TestJsonImporter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            if os.path.exists(TEST_WORKING_DIRECTORY):
                for subDir in os.listdir(TEST_WORKING_DIRECTORY):
                    os.remove(os.path.join(TEST_WORKING_DIRECTORY, subDir))
                # os.rmdir(TEST_WORKING_DIRECTORY)
        except OSError:
            cls.fail(cls, "Cannot Clean up test directory: %s failed" % TEST_WORKING_DIRECTORY)
        try:
            if not os.path.exists(TEST_WORKING_DIRECTORY):
                os.makedirs(TEST_WORKING_DIRECTORY)
        except OSError:
            cls.fail(cls, "Cannot create test directory: %s failed" % TEST_WORKING_DIRECTORY)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        # Close all documents in FreeCAD
        document_list = list(App.listDocuments().keys())
        for document_name in document_list:
            App.closeDocument(document_name)

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
        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = TEST_WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
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
        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = TEST_WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
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
        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = TEST_WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0666dfe022" + FREECAD_FILE_EXTENSION
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
        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = TEST_WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
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
        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = TEST_WORKING_DIRECTORY + "Beam_6201a731_d703_43f8_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "450 mm", "Shape has correctly changed size")
