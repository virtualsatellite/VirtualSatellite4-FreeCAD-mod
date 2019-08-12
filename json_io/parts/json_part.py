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
from abc import ABC


class AJsonPart(ABC):
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
        "length_x": "m",
        "length_y": "m",
        "length_z": "m",
        "radius": "m",
        "color": "rgba"
        }

    def parse_from_json(self, json_object):
        self.name = str(json_object[JSON_ELEMENT_NAME])
        self.shape = str(json_object[JSON_ELEMENT_SHAPE])
        self.uuid = str(json_object[JSON_ELEMENT_UUID]).replace("-", "_")

        # The axis between Virtual Satellite and FreeCAD are not identical
        # Therefore Y and Z gets swpapped here.
        self.length_x = str(json_object[JSON_ELEMENT_LENGTH_X])
        self.length_y = str(json_object[JSON_ELEMENT_LENGTH_Z])
        self.length_z = str(json_object[JSON_ELEMENT_LENGTH_Y])

        self.radius = str(json_object[JSON_ELEMENT_RADIUS])

        # shift from pure rgb to rgba
        self.color = int(json_object[JSON_ELEMENT_COLOR]) << 8

        return self

    def get_shape_type(self):
        shape_type = self.shape.lower().capitalize()
        return shape_type
