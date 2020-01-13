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


import FreeCAD
import FreeCADGui
from freecad.active_document import ActiveDocument
from test.test_setup import AWorkingDirectoryTest
from json_io.json_spread_sheet import JsonSpreadSheet
import json
from json_io.parts.json_part import AJsonPart

App = FreeCAD
Gui = FreeCADGui


class TestJsonSpreadSheet(AWorkingDirectoryTest):

    _json_test_data = """{
        "name": "Beam",
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
        "shape": "BOX",
        "lengthX": 0.04,
        "lengthY": 0.01,
        "lengthZ": 0.3,
        "radius": 0.0,
        "color": 12632256
    }"""

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartSheet/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def setUp(self):
        self._json_test_object = json.loads(self._json_test_data)

    def tearDown(self):
        super().tearDown()

    def test_write_to_freecad(self):
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Write")
        json_part = AJsonPart().parse_from_json(self._json_test_object)
        json_spread_sheet = JsonSpreadSheet(json_part)

        json_spread_sheet_name = json_spread_sheet.create_sheet_name()

        json_part_sheet_object = active_document.app_active_document.getObject(json_spread_sheet_name)
        self.assertIsNone(json_part_sheet_object, "The object does not yet exist")

        json_spread_sheet.write_to_freecad(active_document)

        json_part_sheet_object = active_document.app_active_document.getObject(json_spread_sheet_name)
        self.assertIsNotNone(json_part_sheet_object, "The object does exist now")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 1, "Correct amount of objects in document")
        self.assertEquals(len(json_part_sheet_object.PropertiesList), 36, "Computed correct amount of properties in the sheet")

    def test_read_sheet_attribute(self):
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Read")
        json_part = AJsonPart().parse_from_json(self._json_test_object)
        json_spread_sheet = JsonSpreadSheet(json_part)

        json_spread_sheet.write_to_freecad(active_document)

        attribute = json_spread_sheet.read_sheet_attribute(active_document, "height")

        self.assertEquals(attribute, 300, "Got correct value")

    def test_read_sheet_attribute_from_freecad(self):
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Read")
        json_part = AJsonPart().parse_from_json(self._json_test_object)
        json_spread_sheet = JsonSpreadSheet(json_part)

        json_spread_sheet.write_to_freecad(active_document)

        freecad_sheet = active_document.app_active_document.getObject(json_spread_sheet.create_sheet_name())

        attribute = json_spread_sheet.read_sheet_attribute_from_freecad(freecad_sheet, "height")

        self.assertEquals(attribute, 300, "Got correct value")

    def test_is_sheet_attached(self):
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartSheetTest_Attached")
        json_part = AJsonPart().parse_from_json(self._json_test_object)
        json_spread_sheet = JsonSpreadSheet(json_part)

        self.assertFalse(json_spread_sheet.is_sheet_attached(active_document), "There is no sheet yet")

        json_spread_sheet.write_to_freecad(active_document)

        self.assertTrue(json_spread_sheet.is_sheet_attached(active_document), "Sheet got attached and can be read")
