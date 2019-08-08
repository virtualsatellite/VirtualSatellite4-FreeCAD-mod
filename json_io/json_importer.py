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
from json_io.json_definitions import JSON_ELEMENT_NAME,\
    JSON_ELEMENT_SHAPE,\
    JSON_ELEMENT_UUID, FREECAD_FILE_EXTENSION, JSON_ELEMENT_LENGTH_Z,\
    JSON_ELEMENT_LENGTH_Y, JSON_ELEMENT_LENGTH_X

import FreeCAD
import string

App = FreeCAD


class JsonImporter(object):
    '''
    classdocs
    '''

    working_output_directory: string

    def __init__(self, working_ouput_directory):
        self.working_output_directory = working_ouput_directory

    def create_or_update_part(self, json_object):

        # Retrieve name and shape information from json object
        part_name = str(json_object[JSON_ELEMENT_NAME])
        part_shape = str(json_object[JSON_ELEMENT_SHAPE])
        part_uuid = str(json_object[JSON_ELEMENT_UUID]).replace("-", "_")

        # Use the name to create the part document
        # should be careful in case the name already exists.
        # thus it is combined with the uuid. not really nice
        # but definitely efficient
        part_file_name = str(part_name + "_" + part_uuid)
        App.newDocument(part_file_name)
        App.setActiveDocument(part_file_name)
        App.ActiveDocument = App.getDocument(part_file_name)

        part_file_fullpath = self.working_output_directory + part_file_name + FREECAD_FILE_EXTENSION

        # Dispatch to creation method depending on shape type
        create_or_update_method_name = "create_or_update_" + part_shape.lower()
        create_or_update_dispatch = getattr(self, create_or_update_method_name, lambda: "Invalid call to : " + create_or_update_method_name)
        create_or_update_dispatch(json_object)

        App.getDocument(part_file_name).saveAs(part_file_fullpath)
        print("should have saved")

    def create_or_update_box(self, json_object):
        print("creating a box")
        part_name = json_object[JSON_ELEMENT_NAME]

        App.ActiveDocument.addObject("Part::Box", "Box")
        App.ActiveDocument.ActiveObject.Label = part_name
        App.ActiveDocument.recompute()

        part_length_x = str(json_object[JSON_ELEMENT_LENGTH_X])
        part_length_y = str(json_object[JSON_ELEMENT_LENGTH_Y])
        part_length_z = str(json_object[JSON_ELEMENT_LENGTH_Z])

        App.ActiveDocument.getObject("Box").Length = part_length_x + ' m'
        App.ActiveDocument.getObject("Box").Height = part_length_y + ' m'
        App.ActiveDocument.getObject("Box").Width = part_length_z + ' m'

    def create_or_update_cone(self, json_object):
        pass

    def create_or_update_cylinder(self, json_object):
        pass

    def create_or_update_sphere(self, json_object):
        pass

    def create_or_update_geometry(self, json_object):
        pass
