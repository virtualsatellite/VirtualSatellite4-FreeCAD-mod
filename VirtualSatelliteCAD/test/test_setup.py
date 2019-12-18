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
from copy import deepcopy

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

    def _order(self, obj):
        """
        Recursive orders object with nested lists and dictionaries
        """
        if isinstance(obj, dict):
            return sorted((k, self._order(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self._order(x) for x in obj)
        else:
            return obj

    def assertJsonObjectsEqual(self, first, second, msg=None):
        self.assertEqual(self._order(first), self._order(second), msg)

    def _ignore(self, obj, keys):
        """
        Recursive ignore objects
        keys: URI like "key1.key2" ignores obj["key1"]["key2"]
        """
        key = keys[0]

        if isinstance(obj, dict):
            # last key
            if len(keys) == 1:
                obj[key] = None
            else:
                if key in obj:
                    self._ignore(obj[key], ".".keys[1:])

    def _ignore_static(self, obj, static_keys):
        """
        Recursive ignore objects
        static_keys: list of attributes to be ignored at any position like "*.static_key"
        """

        # dead call if the list is empty
        if(static_keys == []):
            return

        if isinstance(obj, dict):
            for static_key in static_keys:
                if static_key in obj:
                    obj[static_key] = None

            for _, value in obj.items():
                self._ignore_static(value, static_keys)

        elif isinstance(obj, list):
            for item in obj:
                self._ignore_static(item, static_keys)

    def assertJsonObjectsAlmostEqual(self, first, second, diff=[], msg="", static_keys=[]):
        """
        Ignores differences to be specified as URIs like "key1.key2" in diff
        Checks for equality in the resulting JSON objects
        """
        # copy objects so we don't change the real ones
        first_copy, second_copy = deepcopy(first), deepcopy(second)

        for uri in diff:
            keys = uri.split(".")
            self._ignore(first_copy, keys)
            self._ignore(second_copy, keys)

        self._ignore_static(first_copy, static_keys)
        self._ignore_static(second_copy, static_keys)

        self.assertEqual(self._order(first_copy), self._order(second_copy), msg)
