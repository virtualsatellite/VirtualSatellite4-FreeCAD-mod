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

from json_io.json_definitions import JSON_ELEMENT_NAME, JSON_ELEMENT_UUID,\
    JSON_ELEMENT_POS_Y, JSON_ELEMENT_POS_X,\
    JSON_ELEMENT_POS_Z, JSON_ELEMENT_ROT_X, JSON_ELEMENT_ROT_Y,\
    JSON_ELEMENT_ROT_Z, JSON_ELEMENT_PART_UUID, JSON_ELEMENT_PART_NAME, M_TO_MM,\
    RAD_TO_DEG, _get_combined_name_uuid
from json_io.json_spread_sheet import JsonSpreadSheet
from A2plus.a2p_importpart import importPartFromFile
from freecad.active_document import FREECAD_FILE_EXTENSION


class AJsonProduct():

    def __init__(self):
        self.attributes = {
            "name": "-",
            "uuid": "-",
            "part_name": "-",
            "part_uuid": "-",
            "pos_x": "mm",
            "pos_y": "mm",
            "pos_z": "mm",
            "rot_x": "°",
            "rot_y": "°",
            "rot_z": "°",
            }

        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

    def _parse_name_and_uuid_from_json(self, json_object):
        self.name = str(json_object[JSON_ELEMENT_NAME])
        self.uuid = str(json_object[JSON_ELEMENT_UUID]).replace("-", "_")
        self.part_uuid = str(json_object[JSON_ELEMENT_PART_UUID]).replace("-", "_")
        self.part_name = str(json_object[JSON_ELEMENT_PART_NAME]).replace("-", "_")

    def _parse_position_and_rotation_from_json(self, json_object):
        # the coordinate system between virtual satellite and FreeCAD seem
        # to be identical. no Further adjustments or transformations needed.
        self.pos_x = float(json_object[JSON_ELEMENT_POS_X]) * M_TO_MM
        self.pos_y = float(json_object[JSON_ELEMENT_POS_Y]) * M_TO_MM
        self.pos_z = float(json_object[JSON_ELEMENT_POS_Z]) * M_TO_MM

        # the coordinate system between virtual satellite and FreeCAD seem
        # to be identical. no Further adjustments or transformations needed.
        self.rot_x = float(json_object[JSON_ELEMENT_ROT_X]) * RAD_TO_DEG
        self.rot_y = float(json_object[JSON_ELEMENT_ROT_Y]) * RAD_TO_DEG
        self.rot_z = float(json_object[JSON_ELEMENT_ROT_Z]) * RAD_TO_DEG

    def parse_from_json(self, json_object):
        self._parse_name_and_uuid_from_json(json_object)
        self._parse_position_and_rotation_from_json(json_object)
        self.sheet = JsonSpreadSheet(self)

        return self

    def _create_or_update_freecad_part(self, active_document):
        import_part_file_name = self.get_part_unique_name()
        import_part_full_path = active_document.get_file_full_path(import_part_file_name)
        importPartFromFile(active_document.app_active_document, import_part_full_path)

    def _set_freecad_name_and_color(self, active_document):
        pass

    def _set_freecad_properties(self, active_document):
        pass

    def write_to_freecad(self, active_document):
        self._create_or_update_freecad_part(active_document)

        # to the FreeCAD document
        self.sheet.write_to_freecad(active_document)

    def get_unique_name(self):
        '''
        Returns the uniqe name of the current product
        '''
        return _get_combined_name_uuid(self.name, self.uuid)

    def get_part_unique_name(self):
        '''
        Returns the unique name of the referenced part
        '''
        return _get_combined_name_uuid(self.part_name, self.part_uuid)
