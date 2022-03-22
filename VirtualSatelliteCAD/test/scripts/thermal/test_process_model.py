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
from scripts.thermal.process_model import getSunData, getEarthData, findAllContacts,\
    createMeshAndGroupsAndInputFile, hideAllFaces, writeContactToInput, applyVolumeFlux
from json_io.json_importer import JsonImporter
from module.environment import Environment
import json
import shutil
from test.scripts.thermal.test_json_data import JSON_MAKE_CONTACT_FACES
import os
from scripts.thermal.prepare_model import make_contact_faces


class TestProcessModel(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ThermalProcessModel/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def copyTestResource(self, name):
        """
        Copy the test resource in the test working directory
        """
        test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", name))
        shutil.copy(test_resource_path, self._WORKING_DIRECTORY)

    def assertFilesEqualLine(self, name, line):
        test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", name))
        test_file = open(test_resource_path, "r").readlines()
        created_file = open(os.path.join(self._WORKING_DIRECTORY, name)).readlines()
        self.assertEquals(test_file[line], created_file[line])

    def assertFilesEqualContent(self, name):
        test_resource_path = Environment.get_test_resource_path(os.path.join("Thermal", name))
        test_file = open(test_resource_path, "r").read()
        created_file = open(os.path.join(self._WORKING_DIRECTORY, name)).read()
        self.assertEquals(test_file, created_file)

    def importTestJson(self):
        json_importer = JsonImporter(self._WORKING_DIRECTORY)
        json_object = json.loads(JSON_MAKE_CONTACT_FACES)
        json_importer.full_import(json_object)

    def test_getSunData(self):
        self.copyTestResource("Sun_Vector.csv")
        self.copyTestResource("Solar_Intensity.csv")
        sunData = getSunData(self._WORKING_DIRECTORY, "Sun_Vector.csv", "Solar_Intensity.csv")
        self.assertEqual(60, len(sunData), "Extracted 60 entries of sun data")
        self.assertEqual((('130253576.662236', '36557761.626092', '-57757642.069708'), '100.000000'),
                         sunData[0], "Has expected format")

    def test_getEarthData(self):
        self.copyTestResource("Earth_Vector.csv")
        earthData = getEarthData(self._WORKING_DIRECTORY, "Earth_Vector.csv")
        self.assertEqual(60, len(earthData), "Extracted 60 entries of earth data")
        self.assertEqual((('130253576.662236', '36557761.626092', '-57757642.069708'), '0.96'),
                         earthData[0], "Has expected format")

    def test_findAllContacts(self):
        self.importTestJson()

        contactFaces = findAllContacts(self._WORKING_DIRECTORY)
        self.assertEquals(([], [], [], ([], [])), contactFaces, "No contact faces were present")

        self.copyTestResource("validateContactsMaster.txt")
        self.copyTestResource("validateContactsSlave.txt")
        make_contact_faces(self._WORKING_DIRECTORY)
        contactFaces = findAllContacts(self._WORKING_DIRECTORY)

        (masterContactFaces, slaveContactFaces, contactNumber, (masterContactMeshSize, slaveContactMeshSize)) = contactFaces
        self.assertEquals(len(masterContactFaces), 6)
        self.assertEquals(len(slaveContactFaces), 6)
        self.assertEquals(len(contactNumber), 6)
        self.assertEqual(len(masterContactMeshSize), 6)
        self.assertEqual(len(slaveContactMeshSize), 6)

        self.assertEquals(masterContactFaces[0], ['BaseplateXZ_af0a4136___dbc7___441f___9a64___cde9bb47b3b2', 4])
        self.assertEquals(slaveContactFaces[0], ['BaseplateXY_6997d1a8___8859___462d___b50f___1b4ce04208ff', 4])
        self.assertEquals(contactNumber[0], 1)
        self.assertEqual(masterContactMeshSize[0], '0.0')
        self.assertEqual(slaveContactMeshSize[0], '0.0')

    def copyTestResourcesForElement(self, name):
        self.copyTestResource(name + ".rd")
        self.copyTestResource(name + ".ehf")
        self.copyTestResource(name + ".hf")
        self.copyTestResource(name + ".bcf")
        self.copyTestResource(name + ".bc")
        self.copyTestResource(name + ".bfl")

    def test_createMeshAndGroupsAndInputFile(self):
        self.importTestJson()

        self.copyTestResource("validateContactsMaster.txt")
        self.copyTestResource("validateContactsSlave.txt")
        self.copyTestResource("Sun_Vector.csv")
        self.copyTestResource("Solar_Intensity.csv")
        self.copyTestResource("Earth_Vector.csv")
        self.copyTestResource("meshSizes.txt")
        self.copyTestResourcesForElement("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91")
        self.copyTestResourcesForElement("BaseplateXZ_af0a4136_dbc7_441f_9a64_cde9bb47b3b2")
        self.copyTestResourcesForElement("BaseplateXY_6997d1a8_8859_462d_b50f_1b4ce04208ff")
        self.copyTestResourcesForElement("BaseplateYZ_2ff7921c_8971_4de7_93ee_115cdf80eff7")
        self.copyTestResourcesForElement("PayloadScience_d5384e56_711c_4361_b31c_1dde0d3b4784")
        self.copyTestResourcesForElement("PayloadCommunications_9c0e82fc_6ba7_43c9_ba71_a6bdea9974cf")

        sunData = getSunData(self._WORKING_DIRECTORY, "Sun_Vector.csv", "Solar_Intensity.csv")
        earthData = getEarthData(self._WORKING_DIRECTORY, "Earth_Vector.csv")
        make_contact_faces(self._WORKING_DIRECTORY)
        contactFaces = findAllContacts(self._WORKING_DIRECTORY)
        hideAllFaces()

        createMeshAndGroupsAndInputFile(self._WORKING_DIRECTORY, contactFaces, False, sunData, earthData)

        self.assertFilesEqualLine("BaseplateXZ_af0a4136_dbc7_441f_9a64_cde9bb47b3b2.inp", 4)
        self.assertFilesEqualLine("BaseplateXY_6997d1a8_8859_462d_b50f_1b4ce04208ff.inp", 4)
        self.assertFilesEqualLine("BaseplateYZ_2ff7921c_8971_4de7_93ee_115cdf80eff7.inp", 4)
        self.assertFilesEqualLine("PayloadCommunications_9c0e82fc_6ba7_43c9_ba71_a6bdea9974cf.inp", 4)
        self.assertFilesEqualLine("PayloadScience_d5384e56_711c_4361_b31c_1dde0d3b4784.inp", 4)
        self.assertFilesEqualLine("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91.inp", 4)

    def test_writeContactToInput(self):
        self.importTestJson()

        self.copyTestResource("validateContactsMaster.txt")
        self.copyTestResource("validateContactsSlave.txt")
        self.copyTestResource("Sun_Vector.csv")
        self.copyTestResource("Solar_Intensity.csv")
        self.copyTestResource("Earth_Vector.csv")
        self.copyTestResource("meshSizes.txt")
        self.copyTestResourcesForElement("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91")
        self.copyTestResourcesForElement("BaseplateXZ_af0a4136_dbc7_441f_9a64_cde9bb47b3b2")
        self.copyTestResourcesForElement("BaseplateXY_6997d1a8_8859_462d_b50f_1b4ce04208ff")
        self.copyTestResourcesForElement("BaseplateYZ_2ff7921c_8971_4de7_93ee_115cdf80eff7")
        self.copyTestResourcesForElement("PayloadScience_d5384e56_711c_4361_b31c_1dde0d3b4784")
        self.copyTestResourcesForElement("PayloadCommunications_9c0e82fc_6ba7_43c9_ba71_a6bdea9974cf")

        sunData = getSunData(self._WORKING_DIRECTORY, "Sun_Vector.csv", "Solar_Intensity.csv")
        earthData = getEarthData(self._WORKING_DIRECTORY, "Earth_Vector.csv")
        make_contact_faces(self._WORKING_DIRECTORY)
        contactFaces = findAllContacts(self._WORKING_DIRECTORY)
        hideAllFaces()
        createMeshAndGroupsAndInputFile(self._WORKING_DIRECTORY, contactFaces, False, sunData, earthData)

        writeContactToInput(self._WORKING_DIRECTORY, contactFaces)

        self.assertFilesEqualContent("contact_surfaces.inp")

    def test_applyVolumeFlux(self):
        self.importTestJson()

        self.copyTestResource("validateContactsMaster.txt")
        self.copyTestResource("validateContactsSlave.txt")
        self.copyTestResource("Sun_Vector.csv")
        self.copyTestResource("Solar_Intensity.csv")
        self.copyTestResource("Earth_Vector.csv")
        self.copyTestResource("meshSizes.txt")
        self.copyTestResourcesForElement("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91")
        self.copyTestResourcesForElement("BaseplateXZ_af0a4136_dbc7_441f_9a64_cde9bb47b3b2")
        self.copyTestResourcesForElement("BaseplateXY_6997d1a8_8859_462d_b50f_1b4ce04208ff")
        self.copyTestResourcesForElement("BaseplateYZ_2ff7921c_8971_4de7_93ee_115cdf80eff7")
        self.copyTestResourcesForElement("PayloadScience_d5384e56_711c_4361_b31c_1dde0d3b4784")
        self.copyTestResourcesForElement("PayloadCommunications_9c0e82fc_6ba7_43c9_ba71_a6bdea9974cf")

        sunData = getSunData(self._WORKING_DIRECTORY, "Sun_Vector.csv", "Solar_Intensity.csv")
        earthData = getEarthData(self._WORKING_DIRECTORY, "Earth_Vector.csv")
        make_contact_faces(self._WORKING_DIRECTORY)
        contactFaces = findAllContacts(self._WORKING_DIRECTORY)
        hideAllFaces()
        createMeshAndGroupsAndInputFile(self._WORKING_DIRECTORY, contactFaces, False, sunData, earthData)
        writeContactToInput(self._WORKING_DIRECTORY, contactFaces)

        applyVolumeFlux(self._WORKING_DIRECTORY)

        self.assertFilesEqualContent("BaseplateXZ_af0a4136_dbc7_441f_9a64_cde9bb47b3b2.bfl")
        self.assertFilesEqualContent("BaseplateXY_6997d1a8_8859_462d_b50f_1b4ce04208ff.bfl")
        self.assertFilesEqualContent("BaseplateYZ_2ff7921c_8971_4de7_93ee_115cdf80eff7.bfl")
        self.assertFilesEqualContent("PayloadCommunications_9c0e82fc_6ba7_43c9_ba71_a6bdea9974cf.bfl")
        self.assertFilesEqualContent("PayloadScience_d5384e56_711c_4361_b31c_1dde0d3b4784.bfl")
        self.assertFilesEqualContent("PowerBattery_978e1011_778c_48ae_a366_09a283bf0a91.bfl")
