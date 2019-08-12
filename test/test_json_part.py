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

import json
from json_io.parts.json_part import AJsonPart


class TestJsonPart(unittest.TestCase):

    def test_parse(self):
        json_data = """{
            "name": "Beam",
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
            "shape": "BOX",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "color": 12632256
        }"""

        json_object = json.loads(json_data)
        json_part = AJsonPart().parse_from_json(json_object)

        self.assertEqual(json_part.name, "Beam", "Property is correctly set")
        self.assertEqual(json_part.uuid, "6201a731_d703_43f8_ab37_6a0581dfe022", "Property is correctly set")
        self.assertEqual(json_part.shape, "BOX", "Property is correctly set")

        self.assertEqual(json_part.length_x, "0.04", "Property is correctly set")
        self.assertEqual(json_part.length_y, "0.3", "Property is correctly set and axes are swapped")
        self.assertEqual(json_part.length_z, "0.01", "Property is correctly set and axes are swapped")
        self.assertEqual(json_part.radius, "0.0", "Property is correctly set and")

        self.assertEqual(json_part.color, 12632256 << 8, "Property is correctly set")
