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

from json_io.json_definitions import JSON_ELEMENT_NAME, JSON_ELEMENT_SHAPE,\
    JSON_ELEMENT_UUID, JSON_ELEMENT_LENGTH_X, JSON_ELEMENT_LENGTH_Y,\
    JSON_ELEMENT_LENGTH_Z, JSON_ELEMENT_RADIUS, JSON_ELEMENT_COLOR


M_TO_MM = 1000


class AJsonPart():
    '''
    This class translates a json object into a more specific
    one which represents all relevant information of a part. On
    top of that this class will provide additional functionality
    such as swapping the axes if needed as well as cleaning uuid etc.
    '''

    attributes = {
        "name": "-",
        "shape": "-",
        "uuid": "-",
        "length_x": "mm",
        "length_y": "mm",
        "length_z": "mm",
        "radius": "mm",
        "color": "rgba"
        }

    def parse_from_json(self, json_object):
        self.name = str(json_object[JSON_ELEMENT_NAME])
        self.shape = str(json_object[JSON_ELEMENT_SHAPE])
        self.uuid = str(json_object[JSON_ELEMENT_UUID]).replace("-", "_")

        # The axis between Virtual Satellite and FreeCAD are not identical
        # Therefore Y and Z gets swpapped here. We also convert m to mm
        # by definition the values in this part object represent the values
        # as used in FreeCAD
        self.length_x = float(json_object[JSON_ELEMENT_LENGTH_X]) * M_TO_MM
        self.length_y = float(json_object[JSON_ELEMENT_LENGTH_Z]) * M_TO_MM
        self.length_z = float(json_object[JSON_ELEMENT_LENGTH_Y]) * M_TO_MM

        self.radius = float(json_object[JSON_ELEMENT_RADIUS]) * M_TO_MM

        # shift from pure rgb to rgba
        self.color = int(json_object[JSON_ELEMENT_COLOR]) << 8

        return self

    def _create_freecad_object(self, active_document):
        object_name_and_type = self.get_shape_type()
        document_object = active_document.app_active_document.getObject(object_name_and_type)

        if document_object is None:
            object_type = "Part::" + object_name_and_type
            object_name = object_name_and_type
            active_document.app_active_document.addObject(object_type, object_name)

    def _set_freecad_name_and_color(self, active_document):
        object_name_and_type = self.get_shape_type()

        active_document.app_active_document.getObject(object_name_and_type).Label = self.name
        active_document.gui_active_document.getObject(object_name_and_type).ShapeColor = self.color

    def _set_freecad_properties(self, active_document):
        pass

    def write_to_freecad(self, active_document):
        self._create_freecad_object(active_document)
        self._set_freecad_name_and_color(active_document)
        self._set_freecad_properties(active_document)

    def get_shape_type(self):
        shape_type = self.shape.lower().capitalize()
        return shape_type
