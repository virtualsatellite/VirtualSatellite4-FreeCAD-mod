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
from json_io.parts.json_part_cone import JsonPartCone
import FreeCAD
import FreeCADGui

App = FreeCAD
Gui = FreeCADGui


class TestJsonPartCone(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("PartCone/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_create_part_cone(self):
        json_data = """{
            "name": "Beam",
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
            "shape": "CONE",
            "lengthX": 0.0,
            "lengthY": 0.5,
            "lengthZ": 0.0,
            "radius": 0.2,
            "color": 12632256
        }"""

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("PartCone")
        json_object = json.loads(json_data)

        json_part = JsonPartCone()
        json_part.parse_from_json(json_object)
        json_part.write_to_freecad(active_document)

        active_document.save_as("PartCone")

        self.assertIsNotNone(App.ActiveDocument.getObject("Cone"), "The Box object got created")

        # Check that there is a box with the correct properties
        self.assertEquals(App.ActiveDocument.getObject("Cone").Radius1, 0, "Shape has correct size")
        self.assertEquals(App.ActiveDocument.getObject("Cone").Radius2, 200, "Shape has correct size")
        self.assertEquals(App.ActiveDocument.getObject("Cone").Height, 500, "Shape has correct size")

        self.assertEquals(Gui.ActiveDocument.getObject("Cone").ShapeColor,
                          (0.7529411911964417, 0.7529411911964417, 0.7529411911964417, 0.0),
                          "Shape has correct color")
