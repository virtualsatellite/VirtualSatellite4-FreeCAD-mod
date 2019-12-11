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
    JSON_ELEMENT_LENGTH_Z, JSON_ELEMENT_RADIUS, JSON_ELEMENT_COLOR, M_TO_MM,\
    _get_combined_name_uuid, PART_IDENTIFIER
from json_io.json_spread_sheet import JsonSpreadSheet


class AJsonPart():
    '''
    This class translates a json object into a more specific
    one which represents all relevant information of a part. On
    top of that this class will provide additional functionality
    such as swapping the axes if needed as well as cleaning uuid etc.
    '''

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
        '''
        This method parses the properties from the json object as they are needed for FreeCAD
        Transformations are also applied where needed.
        '''
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

    def parse_to_json(self):
        json_dict = {
            JSON_ELEMENT_NAME: self.name,
            JSON_ELEMENT_UUID: self.uuid,
            JSON_ELEMENT_SHAPE: self.shape,

            JSON_ELEMENT_LENGTH_X: self.length / M_TO_MM,
            JSON_ELEMENT_LENGTH_Y: self.width / M_TO_MM,
            JSON_ELEMENT_LENGTH_Z: self.height / M_TO_MM,

            JSON_ELEMENT_RADIUS: self.radius / M_TO_MM,

            JSON_ELEMENT_COLOR: self.color >> 8
        }

        return json_dict

    def _clean_freecad_object(self, active_document):
        '''
        This method checks if the object to be created complies with the one
        mentioned in the sheet, if not it will remove the object to create space for a new one
        '''
        if self.sheet.is_sheet_attached(active_document):
            current_shape_type = self.sheet.read_sheet_attribute(active_document, "shape")
            # if the current shape type is different than the once specified in
            # the json, it means it has been changed and needs to be updated
            # therefore all previous objects should be removed
            if current_shape_type != self.shape:
                root_objects = list(active_document.app_active_document.RootObjects)
                for root_object in root_objects:
                    active_document.app_active_document.removeObject(root_object.Name)

    def _create_freecad_object(self, active_document):
        '''
        This method handles the correct creation of the FreeCAD object depending
        on the primitive or geometry as selected in the Virtual Satellite and
        the json respectively. The primitives have the same name in FreeCAD as in
        Virtual Satellite. Geometries instead need special treatment.
        '''
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

    def _get_freecad_properties(self, freecad_object):
        pass

    def read_from_freecad(self, freecad_object, freecad_sheet):
        """
        TODO
        """
        # TODO: with sheet?
        self.name = freecad_sheet.get("B3")
        self.shape = freecad_sheet.get("B4")
        self.uuid = freecad_sheet.get("B5")

        # init with values of the sheet
        self.length = float(freecad_sheet.get("B6"))
        self.width = float(freecad_sheet.get("B7"))
        self.height = float(freecad_sheet.get("B8"))
        self.radius = float(freecad_sheet.get("B9"))
        self.color = int(freecad_sheet.get("B10"))

        # then overwrite with the values of the freecad object
        self._get_freecad_properties(freecad_object)

        # color belongs to the GUI so don't get it atm

        # TODO:
        self.sheet = None

    def get_shape_type(self):
        shape_type = self.shape.lower().capitalize()
        return shape_type

    def get_unique_name(self):
        return PART_IDENTIFIER + _get_combined_name_uuid(self.name, self.uuid)
