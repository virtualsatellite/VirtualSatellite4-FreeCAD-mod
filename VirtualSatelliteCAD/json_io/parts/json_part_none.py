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
from freecad.active_document import VECTOR_X


class JsonPartNone(AJsonPart):

    def get_shape_type(self):
        shape_type = "Box"
        return shape_type

    def _set_freecad_properties(self, active_document):
        """
        Creates a visible dummy part (box) because the a2plus workbench (used to import part files into products)
        needs at least one visible part to successfully import a file
        """
        object_name_and_type = self.get_shape_type()
        box = active_document.app_active_document.getObject(object_name_and_type)

        box.Length = 0.001
        box.Height = 0.001
        box.Width = 0.001

        # now center the box as in virtual satellite

        # Now virtual satellite axis correction
        # 1. the cone is aligned on the y axis
        # 2. the origin is in the center of it
        # hence:
        # 1. turn it by 90° on the x axis
        # 2. move it forward by half its size on the y axis
        vector_translation = active_document.app.Vector(-self.length/2, -self.width/2, -self.height/2)
        vector_rotation = active_document.app.Rotation(VECTOR_X, 0)

        placement = active_document.app.Placement(
            vector_translation,
            vector_rotation)

        box.Placement = placement

    def _get_freecad_properties(self, none):
        """
        None shape has no additional properties to get from the FreeCAD dummy part
        """
        pass
