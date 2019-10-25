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
from json_io.parts.json_part_factory import JsonPartFactory
from json_io.parts.json_part_box import JsonPartBox
from json_io.parts.json_part_sphere import JsonPartSphere
from json_io.parts.json_part_geometry import JsonPartGeometry
from json_io.parts.json_part_cylinder import JsonPartCylinder
from json_io.parts.json_part_cone import JsonPartCone
from test.json_io.test_json_data import TEST_JSON_PART_BOX, TEST_JSON_PART_CONE,\
    TEST_JSON_PART_CYLINDER, TEST_JSON_PART_SPHERE, TEST_JSON_PART_GEOMETRY,\
    TEST_JSON_PART_NONE


class TestJsonPartFactory(unittest.TestCase):

    def test_create_box(self):
        json_data = TEST_JSON_PART_BOX

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsInstance(json_part, JsonPartBox, "Created correct object")

    def test_create_cone(self):
        json_data = TEST_JSON_PART_CONE

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsInstance(json_part, JsonPartCone, "Created correct object")

    def test_create_cylinder(self):
        json_data = TEST_JSON_PART_CYLINDER

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsInstance(json_part, JsonPartCylinder, "Created correct object")

    def test_create_sphere(self):
        json_data = TEST_JSON_PART_SPHERE

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsInstance(json_part, JsonPartSphere, "Created correct object")

    def test_create_geometry(self):
        json_data = TEST_JSON_PART_GEOMETRY

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsInstance(json_part, JsonPartGeometry, "Created correct object")

    def test_create_none(self):
        json_data = TEST_JSON_PART_NONE

        json_object = json.loads(json_data)
        json_part = JsonPartFactory().create_from_json(json_object)

        self.assertIsNone(json_part, "Created no object")
