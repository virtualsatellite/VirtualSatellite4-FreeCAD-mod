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


def get_mock_api():
    mock_api = Mock(spec=['get_root_seis', 'get_sei', 'get_ca', 'get_resource'])
    return mock_api


def create_sei(uuid, children=[], category_assignments=[], parent=None):
    # For simplicity the uuid is also the name
    return ABeanStructuralElementInstance(
        uuid=uuid, name=uuid, super_seis=[], parent=parent,
        children=children, category_assignments=category_assignments)


def create_ca(uuid):
    # For simplicity the uuid is also the name
    return ABeanCategoryAssignment(uuid, name=uuid)


def create_response(data_dict):
    # Mock the response object
    return SimpleNamespace(data=dumps(data_dict))


# TODO: description
GEOMETRY_BEAN_RESPONSE = SimpleNamespace(data=bytes('raw_data', 'utf-8'))

CA_NO_VIS = create_ca('caNoVis')
CA_NO_VIS_RESPONSE = create_response({
        vc.UUID: 'caNoVis',
        vc.TYPE: 'noVisType'
    })
CA_VIS = create_ca('caVis')
CA_VIS_RESPONSE = create_response({
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
            vc.VALUE:  1.0
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

SEI_EMPTY = create_sei('seiEmpty')
SEI_EMPTY_RESPONSE = create_response({
        vc.UUID: 'seiEmpty',
        vc.CHILDREN: []
    })
SEI_VIS = create_sei('seiVis', [], [CA_VIS], 'rootSeiComplex')

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

COMPLEX_ROOT_SEIS = [ROOT_SEI_COMPLEX, ROOT_SEI_EMPTY]

STL_FILE_PATH = "/tmp/FreeCADtest/VirSatPluginImporter/seiVis.file.stl"
# TODO: use constants
COMPLEX_ROOT_DICT = {
   "Products": {
      "name": "rootSeiComplex",
      "uuid": "rootSeiComplex",
      "children": [
         {
            "name": "seiVis",
            "uuid": "seiVis",
            "children": [],
            "posX":1.0,
            "posY":2.0,
            "posZ":3.0,
            "rotX":0.25,
            "rotY":0.5,
            "rotZ":0.75,
            "partName":"seiVis",
            "partUuid":"seiVis"
         }
      ]
   },
   "Parts": [
      {
         "name": "seiVis",
         "uuid": "seiVis",
         "shape": "GEOMETRY",
         "color": 255,
         "lengthX": 0.1,
         "lengthY": 0.2,
         "lengthZ": 0.3,
         "radius": 0,
         "stlPath": "/tmp/FreeCADtest/VirSatPluginImporter/seiVis.file.stl"
      }
   ]
}
