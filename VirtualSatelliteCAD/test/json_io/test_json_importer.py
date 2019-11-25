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

    def test_create_part_for_none(self):
        json_data = """{
            "color": 12632256,
            "shape": "NONE",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-22a2-ab37-6a0581dfe022"
        }"""

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_22a2_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertFalse(os.path.isfile(test_file_name), "File does not exist on drive")

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
            "stlPath": "Test.stl"
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

    def test_full_import(self):

        json_test_resource_path = Environment.get_test_resource_path("VisCube2.json")
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        part_file_names, json_product, active_document = json_importer.full_import(json_test_resource_path)

        # =========================
        # Check parts

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check each part
        for part_file_name in part_file_names:
            test_file_name = self._WORKING_DIRECTORY + part_file_name + FREECAD_FILE_EXTENSION
            # print(f"{test_file_name}\n")

            # Check the file got created
            self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")

        # =========================
        # Check product

        # Check that the right number of children and root objects got created
        self.assertEquals(len(json_product.children), 5, "Correct amount of children")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 14, "Found correct amount of root objects 7 plus 7 sheets")

        # Check the product root
        product_part_name = json_product.get_unique_name()
        product_object = active_document.app_active_document.getObjectsByLabel(product_part_name)
        self.assertIsNotNone(product_object, "Found an object under the given part name")

        # Check that for each child a file exists
        for child in json_product.children:
            product_object = active_document.app_active_document.getObjectsByLabel(child.get_unique_name())
            # An empty list in python gets asserted to true
            # TODO: this was assertNotNone, which returned true all the time, so xcheck if this mistake was made somewhere else
            self.assertTrue(product_object, "Found an object under the given part name")
            if(child.name == "BeamStructure"):
                # Check that two sub children are found
                self.assertEquals(len(child.children), 2, "Correct amount of children")
                for subchild in child.children:
                    product_object = active_document.app_active_document.getObjectsByLabel(subchild.get_unique_name())
                    self.assertIsNotNone(product_object, "Found an object under the given part name")

                    # Check propagation
                    # poz_z of -500 should be propagated from "BeamStructure"
                    self.assertEqual(subchild.pos_z, 500.0, "Z position got propagated correctly")

    def test_full_import_again(self):
        """
        importing the same file again should not result in changes
        """
        pass
        # TODO: Check double import of the cube: manually double importing creates a wrong vis atm
        json_test_resource_path = Environment.get_test_resource_path("VisCube2.json")
        json_importer = JsonImporter(self._WORKING_DIRECTORY)

        # =========================
        # First import
        part_file_names, json_product, active_document = json_importer.full_import(json_test_resource_path)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 14, "Found correct amount of root objects 7 plus 7 sheets")

        # =========================
        # Second import
        part_file_names2, json_product2, active_document2 = json_importer.full_import(json_test_resource_path)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names2), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product2.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document2.app_active_document.RootObjects), 14, "Found correct amount of root objects 7 plus 7 sheets")

        # =========================
        # Check equality
        self.assertEquals(part_file_names, part_file_names2)

        for i, child1 in enumerate(json_product.children):
            child2 = json_product2.children[i]
            child1.has_equal_values(child2)

    def test_full_import_again_with_changes(self):
        """
        If two files with the same name get imported all elements of the second file should overwrite the elements of the first file,
        but elements existing in the first file (but not in the second file) won't be changed
        """
        pass
