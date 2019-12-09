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
from json_io.json_importer import JsonImporter
from json_io.json_exporter import JsonExporter
from test.json_io.test_json_data import TEST_JSON_FULL_VISCUBE
import json


class TestJsonExporter(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("Exporter/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_full_export(self):
        # import a file

        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(TEST_JSON_FULL_VISCUBE)
        part_file_names, json_product, active_document = json_importer.full_import(json_object)

        json_exporter = JsonExporter(self._WORKING_DIRECTORY)
        exported_json = json_exporter.full_export(active_document)

        # self.assertEqual(exported_json, json_object, "JSON in and out equal each other")
