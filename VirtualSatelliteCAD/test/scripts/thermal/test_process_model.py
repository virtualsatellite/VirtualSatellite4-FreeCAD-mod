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
from scripts.thermal.process_model import process_model
from json_io.json_importer import JsonImporter
from module.environment import Environment
import json
import shutil
from test.scripts.thermal.test_json_data import JSON_MAKE_CONTACT_FACES
import os


class TestProcesseModel(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ThermalProcessModel/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_process_model(self):
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_MAKE_CONTACT_FACES)
        _, _, active_document = json_importer.full_import(json_object)

        # Copy the test resources in the test working directory
        def copyTestResource(name):
            test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", name))
            shutil.copy(test_resource_path, self._WORKING_DIRECTORY)

        copyTestResource("validateContactsMaster.txt")
        copyTestResource("validateContactsSlave.txt")
        copyTestResource("main.inp")
        copyTestResource("Sun_Vector.csv")
        copyTestResource("Solar_Intensity.csv")
        copyTestResource("Earth_Vector.csv")
        copyTestResource("meshSizes.txt")
        copyTestResource("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91.inp")
        copyTestResource("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91.rd")

        process_model(self._WORKING_DIRECTORY)

        # TODO: asserts
