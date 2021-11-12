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
from plugins.VirtualSatelliteRestPlugin.importer import VirSatRestImporter
from test.plugins.VirtualSatelliteRestPlugin.api_mocks import get_mock_api,\
    COMPLEX_ROOT_SEIS, SEI_VIS, SEI_EMPTY, CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE,\
    ROOT_SEI_COMPLEX, GEOMETRY_BEAN_RESPONSE, COMPLEX_ROOT_DICT, STL_FILE_PATH
from test.test_setup import AWorkingDirectoryTest
import os


class TestImporter(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("VirSatPluginImporter/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def test_importToDict(self):
        # Test setup
        mock_api = get_mock_api()
        importer = VirSatRestImporter(self.getDirectoryFullPath(), mock_api, "")

        # Set up mock data
        mock_api.get_root_seis.return_value = COMPLEX_ROOT_SEIS
        mock_api.get_sei.side_effect = [SEI_EMPTY, SEI_VIS]
        mock_api.get_ca.side_effect = [CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE]
        mock_api.get_resource.return_value = GEOMETRY_BEAN_RESPONSE

        returned_dict = importer.importToDict(ROOT_SEI_COMPLEX.uuid)
        self.assertJsonObjectsEqual(COMPLEX_ROOT_DICT, returned_dict, "Returned JSON as expected")
        self.assertTrue(os.path.isfile(STL_FILE_PATH), "File exists on FS")
