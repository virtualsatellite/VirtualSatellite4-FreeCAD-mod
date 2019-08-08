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
from json_io.json_importer import JsonImporter
import json

App = FreeCAD


# define the name of the directory to be created
TEST_WORKING_DIRECTORY = "/tmp/FreeCADtest/"


class TestJsonImporter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            if not os.path.exists(TEST_WORKING_DIRECTORY):
                os.makedirs(TEST_WORKING_DIRECTORY)
        except OSError:
            cls.fail(cls, "Cannot create test directory: %s failed" % TEST_WORKING_DIRECTORY)

    def test_create_part(self):
        json_data = """{
            "color": 12632256,
            "shape": "BOX",
            "name": "Beam",
            "lengthX": 0.04,
            "lengthY": 0.01,
            "lengthZ": 0.3,
            "radius": 0.0,
            "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
        }"""

        json_object = json.loads(json_data)

        json_importer = JsonImporter(TEST_WORKING_DIRECTORY)
        json_importer.create_or_update_part(json_object)
