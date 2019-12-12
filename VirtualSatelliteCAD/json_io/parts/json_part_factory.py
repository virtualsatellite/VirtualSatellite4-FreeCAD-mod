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


from json_io.parts.json_part_box import JsonPartBox
from json_io.parts.json_part_cylinder import JsonPartCylinder
from json_io.parts.json_part_cone import JsonPartCone
from json_io.parts.json_part_sphere import JsonPartSphere
from json_io.json_definitions import JSON_ELEMENT_SHAPE,\
    JSON_ELEMENT_SHAPE_NONE
import FreeCAD
from json_io.parts.json_part_geometry import JsonPartGeometry

Log = FreeCAD.Console.PrintLog
Msg = FreeCAD.Console.PrintMessage
Err = FreeCAD.Console.PrintError
Wrn = FreeCAD.Console.PrintWarning


class JsonPartFactory(object):
    '''
    This class creates the correct shape object depending on the given json.
    '''

    @classmethod
    def create_from_json(cls, json_object):
        Log("Creating part object...\n")
        shape = str(json_object[JSON_ELEMENT_SHAPE])

        if shape != JSON_ELEMENT_SHAPE_NONE:
            # Dispatch to creation method depending on shape type
            create_method_name = "_create_json_part_" + shape.lower()
            create_method_dispatch = getattr(cls, create_method_name, lambda: Err("Invalid call to : " + create_method_name + "\n"))
            json_part_x = create_method_dispatch()
            json_part_x.parse_from_json(json_object)

            Log("Done creating part object.\n")
            return json_part_x
        else:
            Log("No part object created.\n")
            return None

    @classmethod
    def create_from_freecad(cls, freecad_object):
        Log("Reading part object...\n")
        shape = freecad_object.TypeId.split(":")[-1]
        if shape == "Feature":
            # assume geometry
            shape = "Geometry"

        # TODO: JSON_ELEMENT_SHAPE_NONE: can't be exported because no representation in FreeCAD exists?
        create_method_name = "_create_json_part_" + shape.lower()
        create_method_dispatch = getattr(cls, create_method_name, lambda: Err("Invalid call to : " + create_method_name + "\n"))
        part_x = create_method_dispatch()

        return part_x

    @classmethod
    def _create_json_part_box(cls):
        Log("Creating box part.\n")
        return JsonPartBox()

    @classmethod
    def _create_json_part_cylinder(cls):
        Log("Creating cylinder part.\n")
        return JsonPartCylinder()

    @classmethod
    def _create_json_part_cone(cls):
        Log("Creating cone part.\n")
        return JsonPartCone()

    @classmethod
    def _create_json_part_sphere(cls):
        Log("Creating sphere part.\n")
        return JsonPartSphere()

    @classmethod
    def _create_json_part_geometry(cls):
        Log("Creating sphere part.\n")
        return JsonPartGeometry()
