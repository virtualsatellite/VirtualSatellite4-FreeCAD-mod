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
from json_io.parts.json_part_cylinder import JsonPartCylinder

App = FreeCAD
Gui = FreeCADGui


class TestJsonPartCylinder(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartCylinder/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_create_part_cylinder(self):
        json_data = """{
            "color": 12632256,
            "shape": "CYLINDER",
            "name": "Tube",
            "lengthX": 0.0,
            "lengthY": 0.1,
            "lengthZ": 0.0,
            "radius": 0.05,
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
        }"""

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartCylinder")
        json_object = json.loads(json_data)

        json_part = JsonPartCylinder()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        active_document.save_as("PartCylinder")

        self.assertIsNotNone(App.ActiveDocument.getObject("Cylinder"), "The Box object got created")

        # Check that there is a box with the correct properties
        self.assertEquals(App.ActiveDocument.getObject("Cylinder").Radius, 50, "Shape has correct size")
        self.assertEquals(App.ActiveDocument.getObject("Cylinder").Height, 100, "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Cylinder").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")
