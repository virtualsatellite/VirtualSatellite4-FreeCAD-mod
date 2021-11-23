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
from copy import deepcopy
from unittest import TestCase
from unittest.mock import call

import json_io.json_definitions as jd
from plugins.VirtualSatelliteRestPlugin.exporter import VirSatRestExporter
import plugins.VirtualSatelliteRestPlugin.virsat_constants as vc
from test.plugins.VirtualSatelliteRestPlugin.api_mocks import get_mock_api, \
    COMPLEX_ROOT_SEIS, SEI_VIS, SEI_EMPTY, CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE, \
    COMPLEX_ROOT_DICT, \
    ROOT_SEI_COMPLEX_RESPONSE, SEI_VIS_RESPONSE, SEI_VIS_DICT, CA_VIS_DICT


class TestExorter(TestCase):

    def test_exportFromDict(self):
        # Test setup
        mock_api = get_mock_api()
        exporter = VirSatRestExporter()

        # Set up mock data
        mock_api.get_root_seis.return_value = COMPLEX_ROOT_SEIS
        mock_api.get_sei.side_effect = [
            SEI_EMPTY, SEI_VIS,  # Initial tree crawl
            ROOT_SEI_COMPLEX_RESPONSE, SEI_VIS_RESPONSE  # Recurse products
        ]
        mock_api.get_ca.side_effect = [
            CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE,  # Initial tree crawl
        ]
        # mock_api.get_resource.return_value = GEOMETRY_BEAN_RESPONSE

        root_dict = deepcopy(COMPLEX_ROOT_DICT)
        # Simulate changes that should be reflected on the api later:
        # Change the product information
        root_dict[jd.JSON_PRODUCTS][jd.JSON_ELEMNT_CHILDREN][0][jd.JSON_ELEMENT_POS_X] = 0.0
        root_dict[jd.JSON_PARTS][0][jd.JSON_ELEMENT_LENGTH_X] = 0.0
        exporter.exportFromDict(root_dict, mock_api, "")

        # assert correct api calls:
        mock_api.put_sei.assert_called_with(SEI_VIS_DICT, '', _preload_content=False, sync=False)

        dict_changes = deepcopy(CA_VIS_DICT)
        dict_changes[vc.SIZE_X][vc.VALUE] = 0.0
        dict_changes[vc.POSITION_X][vc.VALUE] = 0.0

        expected_calls = [
            # Crawl the tree
            call.get_root_seis(''),
            call.get_ca('caNoVis', '', _preload_content=False, sync=False),
            call.get_sei('seiEmpty', '', sync=False),
            call.get_sei('seiVis', '', sync=False),

            # Update part data of ca
            call.get_ca('caVis', '', _preload_content=False, sync=False),
            # Here we will also see the product changes because it is the same object in the
            # exporter and it will be observed after all operations
            call.put_ca(dict_changes, '', _preload_content=False, sync=False),

            # Recurse products
            call.get_sei('rootSeiComplex', '', _preload_content=False, sync=False),
            call.get_sei('seiVis', '', _preload_content=False, sync=False),
            # Update product data
            call.put_ca(dict_changes, '', _preload_content=False, sync=False),
            call.put_sei(SEI_VIS_DICT, '', _preload_content=False, sync=False),
            call.force_synchronize('')
        ]
        mock_api.assert_has_calls(expected_calls)
