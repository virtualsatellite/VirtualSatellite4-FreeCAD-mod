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
    mock_api = Mock(spec=['get_root_seis', 'get_sei', 'get_ca'])
    return mock_api


def create_sei(uuid, children=[], category_assignments=[]):
    # For simplicity the uuid is also the name
    return ABeanStructuralElementInstance(uuid=uuid, name=uuid, super_seis=[], children=children, category_assignments=category_assignments)


def create_ca(uuid):
    # For simplicity the uuid is also the name
    return ABeanCategoryAssignment(uuid, name=uuid)


def create_response(data_dict):
    # Mock the response object
    return SimpleNamespace(data=dumps(data_dict))


# TODO: description
CA_NO_VIS = create_ca('caNoVis')
CA_NO_VIS_RESPONSE = create_response({
        vc.UUID: 'caNoVis',
        vc.TYPE: 'noVisType'
    })
CA_VIS = create_ca('caVis')
CA_VIS_RESPONSE = create_response({
        vc.UUID: 'caVis',
        vc.TYPE: vc.TYPE_VIS
    })

SEI_EMPTY = create_sei('seiEmpty')
SEI_EMPTY_RESPONSE = create_response({
        vc.UUID: 'seiEmpty',
        vc.CHILDREN: []
    })
SEI_VIS = create_sei('seiVis', [], [CA_VIS])

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
