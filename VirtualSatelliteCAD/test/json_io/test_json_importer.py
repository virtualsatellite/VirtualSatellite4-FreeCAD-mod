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
from freecad.active_document import FREECAD_FILE_EXTENSION, ActiveDocument
from module.environment import Environment
from json_io.json_definitions import JSON_ELEMENT_STL_PATH, PART_IDENTIFIER, PRODUCT_IDENTIFIER, \
    JSON_PARTS, JSON_PRODUCTS, JSON_ELEMNT_CHILDREN, JSON_ELEMENT_ROT_X,\
    JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z, JSON_ELEMENT_POS_X,\
    JSON_ELEMENT_POS_Y, JSON_ELEMENT_POS_Z, JSON_ELEMENT_LENGTH_Y
from test.json_io.test_json_data import TEST_JSON_FULL_VISCUBE, TEST_JSON_FULL_NONE_SHAPE, TEST_JSON_FULL_NONE_SHAPE_ASSEMBLY, \
    TEST_JSON_FULL_GEOMETRY, TEST_JSON_PART_BOX, TEST_JSON_PART_NONE, BEAM_UNIQ_NAME, BEAMSTRUCTURE_UNIQ_NAME, NONE_UNIQ_NAME
from json_io.json_spread_sheet import FREECAD_PART_SHEET_NAME, JsonSpreadSheet
from json_io.parts.json_part_geometry import JsonPartGeometry
from shutil import copyfile

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
        json_data = TEST_JSON_PART_BOX
        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")

        # Check that there is a box with the correct properties
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "40 mm", "Shape has correct size")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Height), "10 mm", "Shape has correct size")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Width), "20 mm", "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Box").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")

    def test_create_part_for_none(self):
        json_data = TEST_JSON_PART_NONE

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check NO file got created
        test_file_name = self._WORKING_DIRECTORY + "Beam_6201a731_d703_22a2_ab37_6a0581dfe022" + FREECAD_FILE_EXTENSION
        self.assertFalse(os.path.isfile(test_file_name), "File does not exist on drive")

    def test_create_part_update_uuid(self):
        '''
        In this test case the uuid is changed. a new uuid has to create a new file.
        '''
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")

        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        App.open(test_file_name)

        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")

    def test_create_part_update_value(self):
        '''
        This test changes an attribute such as the size of the shape.
        Thus the shape is changed but it is still the same object and file.
        '''
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "40 mm", "Shape has correct size")

        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")
        App.open(test_file_name)

        # Check that there is a box with the correct properties
        self.assertEquals(len(App.ActiveDocument.RootObjects), TEST_ALLOWED_AMOUNT_OF_PART_OBJECTS, "Correct amount of objects in file")
        self.assertEquals(str(App.ActiveDocument.getObject("Box").Length), "40 mm", "Shape has correctly changed size")

    def test_create_part_change_shape(self):
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_importer = JsonImporter(self._WORKING_DIRECTORY)

        # get the current module path and get the directory for the test resource
        # place that path into the json object before executing the transformations
        stl_test_resource_path = Environment.get_test_resource_path("Switch.stl")
        json_object[JSON_ELEMENT_STL_PATH] = stl_test_resource_path

        json_importer.create_or_update_part(json_object)

        # Check the file got created
        test_file_name = self._WORKING_DIRECTORY + PART_IDENTIFIER + BEAM_UNIQ_NAME + FREECAD_FILE_EXTENSION
        App.open(test_file_name)

        # Check that there is the correct object inside
        self.assertIsNotNone(App.ActiveDocument.getObject("Box"), "Got correct object")
        App.closeDocument(PART_IDENTIFIER + BEAM_UNIQ_NAME)

        # Now start cyling the objects
        json_object["shape"] = "CYLINDER"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Box"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Cylinder"), "Got correct object")
        App.closeDocument(PART_IDENTIFIER + BEAM_UNIQ_NAME)

        # Next object
        json_object["shape"] = "SPHERE"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Cylinder"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Sphere"), "Got correct object")
        App.closeDocument(PART_IDENTIFIER + BEAM_UNIQ_NAME)

        # Next object
        json_object["shape"] = "GEOMETRY"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Sphere"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Geometry"), "Got correct object")
        App.closeDocument(PART_IDENTIFIER + BEAM_UNIQ_NAME)

        # Next object
        json_object["shape"] = "CONE"
        json_importer.create_or_update_part(json_object)

        # Check that there is the correct object inside
        App.open(test_file_name)
        self.assertIsNone(App.ActiveDocument.getObject("Geometry"), "Removed previous object")
        self.assertIsNotNone(App.ActiveDocument.getObject("Cone"), "Got correct object")
        App.closeDocument(PART_IDENTIFIER + BEAM_UNIQ_NAME)

    def test_full_import(self):
        """
        Full JSON import test
        """

        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        # Check parts
        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check each part
        for part_file_name in part_file_names:
            test_file_name = self._WORKING_DIRECTORY + part_file_name + FREECAD_FILE_EXTENSION

            # Check the file got created
            self.assertTrue(os.path.isfile(test_file_name), "File exists on drive")

        # Check product
        # Check that the right number of children and root objects got created
        self.assertEquals(len(json_product.children), 5, "Correct amount of children")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 10, "Found correct amount of root objects 5 plus 5 sheets")

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
            PRODUCT_IDENTIFIER + BEAMSTRUCTURE_UNIQ_NAME)
        self.assertEquals(len(active_document.app_active_document.RootObjects), 6, "Found correct amount of root objects 3 objects plus 3 sheets")

    def test_full_import_shape_none(self):
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_NONE_SHAPE)
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        self.assertEqual(part_file_names, [PART_IDENTIFIER + NONE_UNIQ_NAME], "Found dummy part")

        self.assertEqual(len(json_product.children), 1, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 2, "Found correct amount of 1 sheet and 1 dummy")

    def test_full_import_shape_none_assembly(self):
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_NONE_SHAPE_ASSEMBLY)
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        self.assertEqual(part_file_names, [PART_IDENTIFIER + NONE_UNIQ_NAME], "Found dummy part")

        self.assertEqual(len(json_product.children), 1, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 2, "Found correct amount of 1 sheet and 1 dummy")

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
                                         PRODUCT_IDENTIFIER + "NoneAssembly_2afb23c9___f458___4bdb___a4e7___fc863364644f")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 4, "Found correct amount of 1 assembly and 2 sheet and 1 dummy")

    def test_full_import_shape_geometry(self):
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_GEOMETRY)

        # get the current module path and get the directory for the test resource
        # place that path into the json object before executing the transformations
        stl_test_resource_path = Environment.get_test_resource_path("Switch.stl")
        stl_test_resource_path_cp = os.path.join(self._WORKING_DIRECTORY, "Switch_cp.stl")
        copyfile(stl_test_resource_path, stl_test_resource_path_cp)
        json_object[JSON_PARTS][0][JSON_ELEMENT_STL_PATH] = stl_test_resource_path_cp

        _, json_product, active_document = json_importer.full_import(json_object)

        self.assertEqual(len(json_product.children), 1, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 2, "Found correct amount of 1 object and 1 sheet")
        name = "Geometry_cc14e2c7___9d7e___4cf2___8d6d___9b8cf5e96d56"
        self.assertEqual(active_document.app_active_document.RootObjects[0].Label, name, "Found the right object")
        self.assertEqual(active_document.app_active_document.RootObjects[1].Label, FREECAD_PART_SHEET_NAME + "_" + name, "Found the right object")

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
            PART_IDENTIFIER + "Geometry_38eae3a5___8338___4a51___b1df___5583058f9e77")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 5, "Found correct amount of 4 object and 1 sheet")

        freecad_sheet = active_document.app_active_document.Objects[4]
        sheet = JsonSpreadSheet(JsonPartGeometry())
        stl_path = sheet.read_sheet_attribute_from_freecad(freecad_sheet, "stl_path")

        # Check that the extra attribute for the STL files got written to the sheet
        self.assertEqual(stl_path, stl_test_resource_path_cp, "The path is written to the spreadsheet")

    def test_full_import_again(self):
        """
        Importing the same file again should not result in changes
        """

        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)

        # =========================
        # First import
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 10, "Found correct amount of root objects 5 plus 5 sheets")

        # Second import
        part_file_names2, json_product2, active_document2 = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names2), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product2.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document2.app_active_document.RootObjects), 10, "Found correct amount of root objects 5 plus 5 sheets")

        # Check equality
        self.assertEquals(part_file_names, part_file_names2)

        for i, child1 in enumerate(json_product.children):
            child2 = json_product2.children[i]
            child1.has_equal_values(child2)

    def test_full_import_again_with_changes_in_product(self):
        """
        After importing the default JSON:
        importing a file with updated product values should result in the values being updated in the FreeCAD object
        """
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)

        # First import
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 10, "Found correct amount of root objects 7 plus 7 sheets")

        # save values of first import
        child = active_document.app_active_document.RootObjects[0]
        child_name = child.Name
        old_rot_x, old_rot_y, old_rot_z = child.Placement.Base
        old_pos_z, old_pos_y, old_pos_x = child.Placement.Rotation.toEuler()

        # Changes in the file
        json_child = json_object[JSON_PRODUCTS][JSON_ELEMNT_CHILDREN][0]

        json_child[JSON_ELEMENT_ROT_X] = 0.5
        json_child[JSON_ELEMENT_ROT_Y] = 0.5
        json_child[JSON_ELEMENT_ROT_Z] = 0.5

        json_child[JSON_ELEMENT_POS_X] = 500
        json_child[JSON_ELEMENT_POS_Y] = 500
        json_child[JSON_ELEMENT_POS_Z] = 500

        # Second import
        part_file_names2, json_product2, active_document2 = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names2), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEquals(len(json_product2.children), 5, "Correct amount of children")
        self.assertEquals(len(active_document2.app_active_document.RootObjects), 10, "Found correct amount of root objects 4 plus 4 sheets")

        # Check children are the same FreeCAD object
        child2 = active_document2.app_active_document.RootObjects[0]
        self.assertEqual(child_name, child2.Name, "Children reference the same FreeCAD object")

        # Check changed values
        new_rot_x, new_rot_y, new_rot_z = child2.Placement.Base
        new_pos_z, new_pos_y, new_pos_x = child2.Placement.Rotation.toEuler()
        self.assertNotAlmostEqual(new_rot_x, old_rot_x, msg="Rotation X changed")
        self.assertNotAlmostEqual(new_rot_y, old_rot_y, msg="Rotation Y changed")
        self.assertNotAlmostEqual(new_rot_z, old_rot_z, msg="Rotation Z changed")

        self.assertNotAlmostEqual(new_pos_x, old_pos_x, msg="Position X changed")
        self.assertNotAlmostEqual(new_pos_y, old_pos_y, msg="Position Y changed")
        self.assertNotAlmostEqual(new_pos_z, old_pos_z, msg="Position Z changed")

    def test_full_import_again_with_changes_in_part(self):
        """
        After importing the default JSON:
        importing a file with updated part values should result in the values being updated in the FreeCAD object.
        Also any additional information provided by the FreeCAD engineer should be lost, except the shape of the object changed
        """
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)

        # First import
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 10, "Found correct amount of root objects 7 plus 7 sheets")

        # save values of first import
        part_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
            PART_IDENTIFIER + BEAMSTRUCTURE_UNIQ_NAME)
        part = part_document.app_active_document.RootObjects[0]
        old_len = part.Height.Value

        # Check that the file is the same and doesn't get cleared by adding a test object
        part_document.app_active_document.addObject("Part::Box", "Test")

        # Changes in the file
        json_object[JSON_PARTS][0][JSON_ELEMENT_LENGTH_Y] = 20

        # Second import
        part_file_names2, json_product2, active_document2 = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names2), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEquals(len(json_product2.children), 5, "Correct amount of children")
        self.assertEquals(len(active_document2.app_active_document.RootObjects), 10, "Found correct amount of root objects 4 plus 4 sheets")

        part_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(
            PART_IDENTIFIER + BEAMSTRUCTURE_UNIQ_NAME)

        # Check that the test object is there
        self.assertEqual(len(part_document.app_active_document.RootObjects), 3, "Found 3 files (2 from the original part and one test object")

        # Check changed values
        part2 = part_document.app_active_document.RootObjects[0]
        new_len = part2.Height.Value
        self.assertNotAlmostEqual(new_len, old_len, msg="Position Z changed")

    def test_full_import_again_with_deletion(self):
        """
        After importing the default JSON:
        importing a file with a missing product (in this case one children) should delete the corresponding FreeCAD object from the assembly
        """
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)

        # First import
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEqual(len(json_product.children), 5, "Correct amount of children")
        self.assertEqual(len(active_document.app_active_document.RootObjects), 10, "Found correct amount of root objects 7 plus 7 sheets")

        # Changes in the file
        # delete first children
        json_object[JSON_PRODUCTS][JSON_ELEMNT_CHILDREN].pop(0)

        # Second import
        part_file_names2, json_product2, active_document2 = json_importer.full_import(json_object)

        # Check that the right number of parts was found
        self.assertEqual(len(part_file_names2), 7, "Found 7 files")

        # Check that the right number of children and root objects got created
        self.assertEquals(len(json_product2.children), 4, "Correct amount of children")
        self.assertEquals(len(active_document2.app_active_document.RootObjects), 8, "Found correct amount of root objects 4 plus 4 sheets")
