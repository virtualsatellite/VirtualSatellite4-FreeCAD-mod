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
from test.test_setup import AWorkingDirectoryTest
from scripts.thermal.prepare_model import make_contact_faces, reset
from json_io.json_importer import JsonImporter
from module.environment import Environment
import json
import shutil
from test.scripts.thermal.test_json_data import JSON_IGNORE_EDGE, JSON_NO_OVERLAP,\
    JSON_MAKE_CONTACT_FACES
import os


class TestPrepareModel(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ThermalPrepareModel/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_make_no_contact_faces_ignore_edge(self):
        # test setup: import the json
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_IGNORE_EDGE)
        _, _, active_document = json_importer.full_import(json_object)

        objectCountBefore = len(active_document.app_active_document.Objects)
        success = make_contact_faces(self._WORKING_DIRECTORY)
        self.assertTrue(success)

        self.assertEqual(len(active_document.app_active_document.BooleanFragments.Objects),
                         2, "Two boolean fragments were created")
        self.assertEqual(len(active_document.app_active_document.Objects),
                         objectCountBefore + 2 + 1, "Only two boolean fragments and a container were created")

    def test_make_no_contact_faces_no_overlap(self):
        # test setup: import the json
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_NO_OVERLAP)
        _, _, active_document = json_importer.full_import(json_object)

        objectCountBefore = len(active_document.app_active_document.Objects)
        success = make_contact_faces(self._WORKING_DIRECTORY)
        self.assertTrue(success)

        self.assertEqual(len(active_document.app_active_document.BooleanFragments.Objects),
                         2, "Two boolean fragments were created")
        self.assertEqual(len(active_document.app_active_document.Objects),
                         objectCountBefore + 2 + 1, "Only two boolean fragments and a container were created")

    def test_make_contact_faces(self):

        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_MAKE_CONTACT_FACES)
        _, _, active_document = json_importer.full_import(json_object)

        # Providing a path missing the expected files returns False if they are needed
        success = make_contact_faces(self._WORKING_DIRECTORY)
        self.assertFalse(success)

        # Copy the test resources in the test working directory
        master_test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", "validateContactsMaster.txt"))
        shutil.copy(master_test_resource_path, self._WORKING_DIRECTORY)
        slaves_test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", "validateContactsSlave.txt"))
        shutil.copy(slaves_test_resource_path, self._WORKING_DIRECTORY)

        objectCountBefore = len(active_document.app_active_document.Objects)
        success = make_contact_faces(self._WORKING_DIRECTORY)
        self.assertTrue(success)

        self.assertEqual(len(active_document.app_active_document.BooleanFragments.Objects),
                         6, "Six boolean fragments were created")
        self.assertEqual(len(active_document.app_active_document.Objects), objectCountBefore + 6 + 1 + 1,
                         "Six boolean fragments, a container and one object for the overlap were created")

    def test_reset(self):

        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_MAKE_CONTACT_FACES)
        _, _, active_document = json_importer.full_import(json_object)

        # Copy the test resources in the test working directory
        master_test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", "validateContactsMaster.txt"))
        shutil.copy(master_test_resource_path, self._WORKING_DIRECTORY)
        slaves_test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", "validateContactsSlave.txt"))
        shutil.copy(slaves_test_resource_path, self._WORKING_DIRECTORY)

        objectCountBefore = len(active_document.app_active_document.Objects)
        success = make_contact_faces(self._WORKING_DIRECTORY)
        self.assertTrue(success)

        self.assertEqual(len(active_document.app_active_document.Objects), objectCountBefore + 6 + 1 + 1,
                         "Six boolean fragments, a container and one object for the overlap were created")

        reset()
        self.assertEqual(len(active_document.app_active_document.Objects), objectCountBefore,
                         "Previous created objects got deleted")
