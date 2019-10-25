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
    RAD_TO_DEG, _get_combined_name_uuid, JSON_ELEMNT_CHILDREN
from json_io.json_spread_sheet import JsonSpreadSheet
from A2plus.a2p_importpart import importPartFromFile
from freecad.active_document import VECTOR_X, VECTOR_Y, VECTOR_Z, VECTOR_ZERO


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

        json_has_part_uuid = JSON_ELEMENT_PART_UUID in json_object
        json_has_part_name = JSON_ELEMENT_PART_NAME in json_object

        if json_has_part_name and json_has_part_uuid:
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

        # Remember if the current project has children or not
        self.has_children = len(list(json_object[JSON_ELEMNT_CHILDREN])) != 0

        return self

    def _create_or_update_freecad_part(self, active_document):
        '''
        This method imports the part referenced by the product.
        The referenced part will be placed under the product part name into
        the assembly. E.g. A BasePlate will be added as BasePlateBottom to the
        assembly. In case the object already exists, nothing special will happen.
        '''
        import_part_file_name = self.get_part_unique_name()
        import_part_name_in_product = self.get_unique_name()
        import_part_full_path = active_document.get_file_full_path(import_part_file_name)
        imported_product_part = importPartFromFile(
            active_document.app_active_document,
            import_part_full_path)
        imported_product_part.Label = import_part_name_in_product

    def _set_freecad_name_and_color(self, active_document):
        pass

    def _set_freecad_position_and_rotation(self, active_document):
        product_part_name = self.get_unique_name()

        product_part = active_document.app_active_document.getObjectsByLabel(product_part_name)[0]

        # First translate than rotate around X, Y and Z
        vector_translation = active_document.app.Vector(self.pos_x, self.pos_y, self.pos_z)
        vector_rotation_zero = active_document.app.Rotation(VECTOR_ZERO, 0)
        vector_rotation_x = active_document.app.Rotation(VECTOR_X, self.rot_x)
        vector_rotation_y = active_document.app.Rotation(VECTOR_Y, self.rot_y)
        vector_rotation_z = active_document.app.Rotation(VECTOR_Z, self.rot_z)

        placement = product_part.Placement

        placement_translation = active_document.app.Placement(
            vector_translation,
            vector_rotation_zero,
            VECTOR_ZERO)

        placement_rotation_x = active_document.app.Placement(
            VECTOR_ZERO,
            vector_rotation_x,
            VECTOR_ZERO)

        placement_rotation_y = active_document.app.Placement(
            VECTOR_ZERO,
            vector_rotation_y,
            VECTOR_ZERO)

        placement_rotation_z = active_document.app.Placement(
            VECTOR_ZERO,
            vector_rotation_z,
            VECTOR_ZERO)

        placement = placement_rotation_x.multiply(placement)
        placement = placement_rotation_y.multiply(placement)
        placement = placement_rotation_z.multiply(placement)
        placement = placement_translation.multiply(placement)

        product_part.Placement = placement

    def write_to_freecad(self, active_document):
        self._create_or_update_freecad_part(active_document)
        self._set_freecad_position_and_rotation(active_document)
        # to the FreeCAD document
        self.sheet.write_to_freecad(active_document)

    def get_unique_name(self):
        '''
        Returns the unique name of the current product
        '''
        return _get_combined_name_uuid(self.name, self.uuid)

    def get_part_unique_name(self):
        '''
        Returns the unique name of the referenced part
        '''
        return _get_combined_name_uuid(self.part_name, self.part_uuid)

    def is_part_reference(self):
        '''
        This method checks for the existence of the properties partUuid and partName.
        In case they are both present, the current product directly references a apart
        '''
        has_part_uuid = hasattr(self, "part_uuid")
        has_part_name = hasattr(self, "part_name")

        return has_part_uuid and has_part_name
