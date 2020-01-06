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


from json_io.parts.json_part import AJsonPart
from json_io.json_definitions import JSON_ELEMENT_STL_PATH
import Mesh, MeshPart # NOQA @UnresolvedImport
import Part  # NOQA @UnusedImport
import os


class JsonPartGeometry(AJsonPart):

    def __init__(self):
        # register the new attribute for the geometries to make sure
        # the value gets exported into the spread sheet as well
        super().__init__()
        self.attributes["stl_path"] = "-"

    def parse_from_json(self, json_object):
        super().parse_from_json(json_object)
        self.stl_path = json_object[JSON_ELEMENT_STL_PATH]

    def parse_to_json(self):
        json_dict = super().parse_to_json()
        json_dict[JSON_ELEMENT_STL_PATH] = self.stl_path

        return json_dict

    def read_from_freecad(self, freecad_object, freecad_sheet):
        super().read_from_freecad(freecad_object, freecad_sheet)

        # use already read in sheet
        self.stl_path = self.sheet.read_sheet_attribute_from_freecad(freecad_sheet, "stl_path")

        # TODO: here?
        self._export_to_stl(freecad_object)

    # this part has no FreeCAD properties
    def _set_freecad_properties(self, active_document):
        pass

    def _get_freecad_properties(self, geometry):
        pass

    def _get_geometry_name(self):
        geometry_full_path = self.stl_path
        geometry_base_name = os.path.basename(geometry_full_path)
        geometry_file_name = os.path.splitext(geometry_base_name)[0]
        return geometry_file_name

    def _create_freecad_object(self, active_document):
        object_name_and_type = self.get_shape_type()
        object_geometry_name = self._get_geometry_name()
        document_object = active_document.app_active_document.getObject(object_name_and_type)

        if document_object is None:
            # Import the mesh
            Mesh.insert(self.stl_path)
            meshed_object = active_document.app_active_document.getObject(object_geometry_name)
            meshed_object.Label = object_geometry_name + "_mesh"

            # Make form out of the mesh
            shape_form = Part.Shape()
            shape_form.makeShapeFromMesh(meshed_object.Mesh.Topology, 0.100000)
            active_document.app_active_document.addObject("Part::Feature", object_geometry_name + "_form").Shape = shape_form

            # Now clean the shape
            shape_cleaned = shape_form.removeSplitter()
            active_document.app_active_document.addObject("Part::Feature", object_geometry_name + "_cleaned").Shape = shape_cleaned

            # Now create the solid
            shape_solid = Part.Solid(shape_cleaned)
            active_document.app_active_document.addObject("Part::Feature", "Geometry").Shape = shape_solid

            # Hide origin objects
            active_document.gui_active_document.getObject(object_geometry_name).Visibility = False
            active_document.gui_active_document.getObject(object_geometry_name + "_form").Visibility = False
            active_document.gui_active_document.getObject(object_geometry_name + "_cleaned").Visibility = False

    def _export_to_stl(self, freecad_object):

        # object_name_and_type = self.get_shape_type()
        # document_object = active_document.app_active_document.getObject(object_name_and_type)

        if freecad_object is not None:
            shape = freecad_object.Shape

            meshed_object = freecad_object.Document.addObject("Mesh::Feature", "Mesh")
            meshed_object.Mesh = MeshPart.meshFromShape(Shape=shape, MaxLength=520)

            meshed_object.Mesh.write(self.stl_path)
