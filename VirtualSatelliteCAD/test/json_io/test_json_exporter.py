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
from json_io.json_definitions import JSON_PRODUCTS, JSON_ELEMNT_CHILDREN, JSON_ELEMENT_NAME, \
    JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z
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
        _, _, active_document = json_importer.full_import(json_object)

        json_exporter = JsonExporter(self._WORKING_DIRECTORY)
        exported_json = json_exporter.full_export(active_document)

        # ignore rotation because of float rounding
        static_keys = [JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y, JSON_ELEMENT_ROT_Z]
        self.assertJsonObjectsAlmostEqual(exported_json, json_object, [], "JSON in and out equal each other", static_keys)

        for child in exported_json[JSON_PRODUCTS][JSON_ELEMNT_CHILDREN]:
            if(child[JSON_ELEMENT_NAME] == "BeamStructure"):
                exported_child = child[JSON_ELEMNT_CHILDREN][0]

        for child in json_object[JSON_PRODUCTS][JSON_ELEMNT_CHILDREN]:
            if(child[JSON_ELEMENT_NAME] == "BeamStructure"):
                json_child = child[JSON_ELEMNT_CHILDREN][0]

        # check rotation
        self.assertAlmostEqual(exported_child[JSON_ELEMENT_ROT_X], json_child[JSON_ELEMENT_ROT_X], msg="Rotation X equal")
        self.assertAlmostEqual(exported_child[JSON_ELEMENT_ROT_Y], json_child[JSON_ELEMENT_ROT_Y], msg="Rotation Y equal")
        self.assertAlmostEqual(exported_child[JSON_ELEMENT_ROT_Z], json_child[JSON_ELEMENT_ROT_Z], msg="Rotation Z equal")

    # TODO:
    def test_full_export_shape_none(self):
        pass

    def test_full_export_shape_geometry(self):
        pass
