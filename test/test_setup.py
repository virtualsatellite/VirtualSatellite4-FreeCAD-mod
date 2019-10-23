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

import FreeCAD
import FreeCADGui
from freecad.active_document import ActiveDocument
import json
from json_io.parts.json_part_box import JsonPartBox

App = FreeCAD
Gui = FreeCADGui


# define the name of the directory to be created
TEST_WORKING_BASE_DIRECTORY = "/tmp/FreeCADtest/"


class AWorkingDirectoryTest(unittest.TestCase):

    @classmethod
    def setUpDirectory(cls, working_directory):
        cls._working_directory = working_directory
        cls._working_directory_full_path = TEST_WORKING_BASE_DIRECTORY + cls._working_directory
        try:
            if os.path.exists(cls._working_directory_full_path):
                for subDir in os.listdir(cls._working_directory_full_path):
                    os.remove(os.path.join(cls._working_directory_full_path, subDir))
                # os.rmdir(TEST_WORKING_BASE_DIRECTORY)
        except OSError:
            cls.fail(cls, "Cannot Clean up test directory: %s failed" % cls._working_directory_full_path)
        try:
            if not os.path.exists(cls._working_directory_full_path):
                os.makedirs(cls._working_directory_full_path)
        except OSError:
            cls.fail(cls, "Cannot create test directory: %s failed" % cls._working_directory_full_path)

    @classmethod
    def getDirectory(cls):
        return cls._working_directory

    @classmethod
    def getDirectoryFullPath(cls):
        return cls._working_directory_full_path

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        # Close all documents in FreeCAD
        document_list = list(App.listDocuments().keys())
        for document_name in document_list:
            App.closeDocument(document_name)

    def create_Test_Part(self):
        '''
        Method to create and store a test part, as it is needed in the assembly tests
        '''
        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "BasePlate",
            "lengthX": 0.04,
            "lengthY": 0.02,
            "lengthZ": 0.002,
            "radius": 0.0,
            "uuid": "3d3708fd-5c6c-4af9-b710-d68778466084"
        }"""

        json_object = json.loads(json_data)
        json_part = JsonPartBox()
        json_part.parse_from_json(json_object)

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document(json_part.get_unique_name())
        json_part.write_to_freecad(active_document)
        active_document.save_and_close_active_document(json_part.get_unique_name())

    def assertAlmostEqualVector(self, first, second, places=7, msg=None):
        '''
        This method helps to make sure, that the content of two array is numerical correct
        and as expected.
        '''
        self.assertEqual(len(first), len(second), msg)
        for index in range(len(first)):
            self.assertAlmostEqual(first[index], second[index], places, msg)
