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
import math
import freecad.name_converter as nc


M_TO_MM = 1000

RAD_TO_DEG = 180.0 / math.pi

JSON_PARTS = "Parts"
JSON_PRODUCTS = "Products"

JSON_ELEMENT_COLOR = "color"
JSON_ELEMENT_SHAPE = "shape"

JSON_ELEMENT_SHAPE_NONE = "NONE"
JSON_ELEMENT_SHAPE_BOX = "BOX"
JSON_ELEMENT_SHAPE_CONE = "CONE"
JSON_ELEMENT_SHAPE_CYLINDER = "CYLINDER"
JSON_ELEMENT_SHAPE_SPHERE = "SPHERE"
JSON_ELEMENT_SHAPE_GEOMETRY = "GEOMETRY"

JSON_ELEMENT_NAME = "name"

JSON_ELEMENT_LENGTH_X = "lengthX"
JSON_ELEMENT_LENGTH_Y = "lengthY"
JSON_ELEMENT_LENGTH_Z = "lengthZ"

JSON_ELEMENT_RADIUS = "radius"
JSON_ELEMENT_UUID = "uuid"

JSON_ELEMENT_STL_PATH = "stlPath"

JSON_ELEMENT_POS_X = "posX"
JSON_ELEMENT_POS_Y = "posY"
JSON_ELEMENT_POS_Z = "posZ"

JSON_ELEMENT_ROT_X = "rotX"
JSON_ELEMENT_ROT_Y = "rotY"
JSON_ELEMENT_ROT_Z = "rotZ"

JSON_ELEMENT_PART_UUID = "partUuid"
JSON_ELEMENT_PART_NAME = "partName"

JSON_ELEMNT_CHILDREN = "children"

PART_IDENTIFIER = "part_"
PRODUCT_IDENTIFIER = "assembly_"


def _get_combined_name_uuid(name, uuid):
    return str(nc.toFreeCad(name) + "_" + nc.toFreeCad(uuid))


def _get_element_name_uuid(json_object):
    name = json_object[JSON_ELEMENT_NAME]
    uuid = json_object[JSON_ELEMENT_UUID]
    return _get_combined_name_uuid(name, uuid)


def get_product_name_uuid(json_object):
    return _get_element_name_uuid(json_object)


def get_part_name_uuid(json_object):
    return _get_element_name_uuid(json_object)


def get_product_part_name_uuid(json_object):
    name = json_object[JSON_ELEMENT_PART_NAME]
    uuid = json_object[JSON_ELEMENT_PART_UUID]
    return _get_combined_name_uuid(name, uuid)
