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


import json
from test.test_setup import AWorkingDirectoryTest
from freecad.active_document import ActiveDocument
import FreeCAD
import FreeCADGui
from json_io.parts.json_part_box import JsonPartBox

App = FreeCAD
Gui = FreeCADGui


class TestJsonPartBox(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartBox/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_create_part_box(self):
        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.02,
            "lengthZ": 0.01,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
        }"""

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartBox")
        json_object = json.loads(json_data)

        json_part = JsonPartBox()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        self.assertIsNotNone(App.ActiveDocument.getObject("Box"), "The Box object got created")

        # Check that there is a box with the correct properties
        self.assertEquals(App.ActiveDocument.getObject("Box").Length, 40, "Shape has correct size")
        self.assertEquals(App.ActiveDocument.getObject("Box").Width, 20, "Shape has correct size")
        self.assertEquals(App.ActiveDocument.getObject("Box").Height, 10, "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Box").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")

        active_document.save_and_close_active_document("PartBox")
