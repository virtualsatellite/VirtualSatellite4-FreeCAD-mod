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
from json_io.parts.json_part_sheet import JsonSpreadSheet


M_TO_MM = 1000


class AJsonProduct():
    
    def __init__(self):
        self.attributes = {
            "name": "-",
            "shape": "-",
            "uuid": "-",
            "length": "mm",
            "width": "mm",
            "height": "mm",
            "radius": "mm",
            "color": "rgba"
            }

    def parse_from_json(self, json_object):
    
        self.name = str(json_object[JSON_ELEMENT_NAME])
        self.shape = str(json_object[JSON_ELEMENT_SHAPE])
        self.uuid = str(json_object[JSON_ELEMENT_UUID]).replace("-", "_")

        # the coordinate system between virtual satellite and FreeCAD seem
        # to be identical. no Further adjustments or transformations needed.
        self.length = float(json_object[JSON_ELEMENT_LENGTH_X]) * M_TO_MM
        self.width = float(json_object[JSON_ELEMENT_LENGTH_Y]) * M_TO_MM
        self.height = float(json_object[JSON_ELEMENT_LENGTH_Z]) * M_TO_MM

        self.radius = float(json_object[JSON_ELEMENT_RADIUS]) * M_TO_MM

        # shift from pure rgb to rgba
        self.color = int(json_object[JSON_ELEMENT_COLOR]) << 8

        self.sheet = JsonSpreadSheet(self)

        return self

    def _clean_freecad_object(self, active_document):
        pass

    def _create_freecad_object(self, active_document):
        pass
    
    def _set_freecad_name_and_color(self, active_document):
        pass
    
    def _set_freecad_properties(self, active_document):
        pass

    def write_to_freecad(self, active_document):
        '''
        This method uses all information from this json part to create
        the corresponding object in FreeCAD.
        '''
        # Create the FreeCAD object and set its properties
        self._clean_freecad_object(active_document)
        self._create_freecad_object(active_document)
        self._set_freecad_name_and_color(active_document)
        self._set_freecad_properties(active_document)

        # Attach the Spreadsheet with a copy of all relevant parameters
        # to the FreeCAD document
        self.sheet.write_to_freecad(active_document)

        # Recompute the object on FreeCAD side
        object_name_and_type = self.get_shape_type()
        active_document.app_active_document.getObject(object_name_and_type).recompute()

