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

from unittest.mock import Mock
from plugins.VirtualSatelliteRestPlugin.generated_api.v0_0_1.swagger_client.models.a_bean_structural_element_instance import ABeanStructuralElementInstance
from plugins.VirtualSatelliteRestPlugin.generated_api.v0_0_1.swagger_client.models.a_bean_category_assignment import ABeanCategoryAssignment
import plugins.VirtualSatelliteRestPlugin.virsat_constants as vc
from json import dumps
from types import SimpleNamespace
import json_io.json_definitions as jd


def get_mock_api():
    mock_api = Mock(spec=['get_root_seis', 'get_sei', 'get_ca', 'get_resource',
                          'put_sei', 'put_ca', 'force_synchronize'])
    return mock_api


def create_sei(uuid, children=[], category_assignments=[], parent=None):
    # For simplicity the uuid is also the name
    return ABeanStructuralElementInstance(
        uuid=uuid, name=uuid, super_seis=[], parent=parent,
        children=children, category_assignments=category_assignments)


def create_ca(uuid):
    # For simplicity the uuid is also the name
    return ABeanCategoryAssignment(uuid, name=uuid)


def uuid_as_name(data_dict):
    data_dict[vc.NAME] = data_dict[vc.UUID]
    return data_dict


def create_response(data_dict):
    # Mock the response object
    return SimpleNamespace(data=dumps(data_dict))


# Now following are test resources, either:
# - In code objects
# - Their raw JSON data (_DICT)
# - Their raw data wrapped in response objects as the API would return them (_RESPONSE)

# Geometry data
GEOMETRY_BEAN_RESPONSE = SimpleNamespace(data=bytes('raw_data', 'utf-8'))

# Category assignments
CA_NO_VIS = create_ca('caNoVis')
CA_NO_VIS_RESPONSE = create_response({
        vc.UUID: 'caNoVis',
        vc.TYPE: 'noVisType'
    })
CA_VIS = create_ca('caVis')
CA_VIS_DICT = uuid_as_name({
        vc.UUID: 'caVis',
        vc.TYPE: vc.TYPE_VIS,
        vc.SHAPE:  {
            vc.VALUE: 'GEOMETRY',
            vc.OVERRIDE: False
        },
        vc.COLOR:  {
            vc.VALUE: 255,
            vc.OVERRIDE: False
        },
        vc.SIZE_X:  {
            vc.VALUE: 0.1,
            vc.OVERRIDE: False
        },
        vc.SIZE_Y:  {
            vc.VALUE: 0.2,
            vc.OVERRIDE: False
        },
        vc.SIZE_Z:  {
            vc.VALUE: 0.3,
            vc.OVERRIDE: False
        },
        vc.RADIUS:  {
            vc.VALUE: 0,
            vc.OVERRIDE: False
        },
        vc.POSITION_X: {
            vc.VALUE: 1.0
        },
        vc.POSITION_Y: {
            vc.VALUE: 2.0
        },
        vc.POSITION_Z: {
            vc.VALUE: 3.0
        },
        vc.ROTATION_X: {
            vc.VALUE: 0.25
        },
        vc.ROTATION_Y: {
            vc.VALUE: 0.5
        },
        vc.ROTATION_Z: {
            vc.VALUE: 0.75
        },
        vc.GEOMETRY: {
            vc.VALUE: 'some/path/file.stl',
            vc.UUID: 'geometryBean',
            vc.OVERRIDE: False
        }
    })
CA_VIS_RESPONSE = create_response(CA_VIS_DICT)

# Seis
SEI_EMPTY = create_sei('seiEmpty')
SEI_EMPTY_RESPONSE = create_response({
        vc.UUID: 'seiEmpty',
        vc.CHILDREN: []
    })
SEI_VIS = create_sei('seiVis', [], [CA_VIS], 'rootSeiComplex')
SEI_VIS_DICT = uuid_as_name({
        vc.UUID: 'seiVis',
        vc.CHILDREN: []
    })
SEI_VIS_RESPONSE = create_response(SEI_VIS_DICT)

# Root seis
ROOT_SEI_EMPTY = create_sei('rootSeiEmpty')
ROOT_SEI_EMPTY_RESPONSE = create_response({
        vc.UUID: 'rootSeiEmpty',
        vc.CHILDREN: []
    })
ROOT_SEI_CHILD = create_sei('rootSeiChild', [SEI_EMPTY])
ROOT_SEI_CHILD_RESPONSE = create_response({
        vc.UUID: 'rootSeiChild',
        vc.CHILDREN: [{
            vc.UUID: 'seiEmpty'
        }]
    })
ROOT_SEI_CA = create_sei('rootSeiCa', [], [CA_NO_VIS])
ROOT_SEI_CAS = create_sei('rootSeiCas', [], [CA_VIS, CA_NO_VIS])
ROOT_SEI_COMPLEX = create_sei('rootSeiComplex', [SEI_EMPTY, SEI_VIS], [CA_NO_VIS])
ROOT_SEI_COMPLEX_RESPONSE = create_response({
        vc.UUID: 'rootSeiComplex',
        vc.CHILDREN: [{
            vc.UUID: 'seiEmpty'
        }, {
            vc.UUID: 'seiVis'
        }]
    })

COMPLEX_ROOT_SEIS = [ROOT_SEI_COMPLEX, ROOT_SEI_EMPTY]

# Internal representation of the API data mocked above
COMPLEX_ROOT_DICT = {
   jd.JSON_PRODUCTS: {
      jd.JSON_ELEMENT_NAME: "rootSeiComplex",
      jd.JSON_ELEMENT_UUID: "rootSeiComplex",
      jd.JSON_ELEMNT_CHILDREN: [
         {
            jd.JSON_ELEMENT_NAME: "seiVis",
            jd.JSON_ELEMENT_UUID: "seiVis",
            jd.JSON_ELEMNT_CHILDREN: [],
            jd.JSON_ELEMENT_POS_X:1.0,
            jd.JSON_ELEMENT_POS_Y:2.0,
            jd.JSON_ELEMENT_POS_Z:3.0,
            jd.JSON_ELEMENT_ROT_X:0.25,
            jd.JSON_ELEMENT_ROT_Y:0.5,
            jd.JSON_ELEMENT_ROT_Z:0.75,
            jd.JSON_ELEMENT_PART_NAME:"seiVis",
            jd.JSON_ELEMENT_PART_UUID:"seiVis"
         }
      ]
   },
   jd.JSON_PARTS: [
      {
         jd.JSON_ELEMENT_NAME: "seiVis",
         jd.JSON_ELEMENT_UUID: "seiVis",
         jd.JSON_ELEMENT_SHAPE: "GEOMETRY",
         jd.JSON_ELEMENT_COLOR: 255,
         jd.JSON_ELEMENT_LENGTH_X: 0.1,
         jd.JSON_ELEMENT_LENGTH_Y: 0.2,
         jd.JSON_ELEMENT_LENGTH_Z: 0.3,
         jd.JSON_ELEMENT_RADIUS: 0,
         jd.JSON_ELEMENT_STL_PATH: "/tmp/FreeCADtest/VirSatPluginImporter/seiVis.file.stl"
      }
   ]
}
