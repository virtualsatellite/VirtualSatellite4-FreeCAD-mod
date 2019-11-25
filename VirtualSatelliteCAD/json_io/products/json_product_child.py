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

from json_io.products.json_product import AJsonProduct
from json_io.json_definitions import _get_combined_name_uuid
from json_io.json_definitions import JSON_ELEMNT_CHILDREN


class JsonProductChild(AJsonProduct):

    def get_part_unique_name(self):
        '''
        Returns the unique name of the referenced part in case it has no children.
        In case it has children, we know that this is a sub assembly or an assembly.
        In this case the file name of the product has to be returned
        '''
        if self.has_children:
            return _get_combined_name_uuid(self.name, self.uuid)
        else:
            return _get_combined_name_uuid(self.part_name, self.part_uuid)

    def parse_from_json(self, json_object):

        super().parse_from_json(json_object)
        if self.has_children:
            # Get all children from the json and try to parse them
            # into JsonProductChild objects
            json_object_children = list(json_object[JSON_ELEMNT_CHILDREN])

            self.children = []
            for json_object_child in json_object_children:

                json_product_child = JsonProductChild().parse_from_json(json_object_child)
                json_product_child.propagate_pos_and_rot_from_parent(self)
                self.children.append(json_product_child)

        return self

    def write_to_freecad(self, active_document):
        # This assembly may refer to a part as well
        # hence if there is a partUuid and if there is a part name, than
        # it should be written to the FreeCAD document as well.
        if self.is_part_reference():
            super().write_to_freecad(active_document)

        # And now write the children, they decide on their own if they reference
        # part or a product
        if self.has_children:
            for child in self.children:
                child.write_to_freecad(active_document)

    def propagate_pos_and_rot_from_parent(self, parent):
        """
        TODO:
        This function propagates position and rotation parameters from the parent:
        Doing this the pos and rot of an object become absolute not relative, which could result
        in overhead when parsing back.
        The question occurs how we handle this problems:
        - Does a product hold its relative and absolute position?
        - if yes how do we keep them in sync
        - ideal would be to only show relative positions to the FreeCAD user and compute them
         to absolute positions internally
        - is that possible with freecad? it seems to only accept absolute positions and no inheritance
        - constraints???
        """
        self.pos_x += parent.pos_x
        self.pos_y += parent.pos_y
        self.pos_z += parent.pos_z

        self.rot_x += parent.rot_x
        self.rot_y += parent.rot_y
        self.rot_z += parent.rot_z
