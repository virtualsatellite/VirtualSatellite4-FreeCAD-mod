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
from json_io.json_definitions import JSON_ELEMNT_CHILDREN
from json_io.products.json_product_child import JsonProductChild


class JsonProductAssembly(AJsonProduct):
    '''
    This class represents an assembly, which consists of several children
    which basically reference the parts to be imported to this assembly.
    The parts/children contain information about their position and orientation.
    This information is processed to correctly place the parts in the assembly.
    The assembly itself can also have a referenced part. But his one does
    not contain information about its position and rotation. In the current assembly,
    this part is supposed to be imported in the current origin of the assembly.
    In case this assembly is a sub assembly it may have a position and rotation.
    Nevertheless in this particular case, the whole assembly is supposed to be positioned
    and rotated in the super assembly. Actually this assembly is than a child product of
    the super assembly.
    '''

    def _parse_position_and_rotation_from_json(self, json_object):
        '''
        An assembly does not have a position or orientation. If it has these properties
        than it is a sub assembly which has to be processed as a child of the containing
        super assembly.
        '''
        pass

    def parse_from_json(self, json_object):
        '''
        This time the parse method follows the convention
        to not parse the position and orientation. Actually it gets called
        in the super method which refers to the protected method for
        importing position and orientation. This method is overridden in this
        class without implementation. Additionally this method starts parsing
        the children.
        '''
        super().parse_from_json(json_object)

        # Get all children from the json and try to parse them
        # into JsonProductChild objects
        json_object_children = list(json_object[JSON_ELEMNT_CHILDREN])

        self.children = []
        for json_object_child in json_object_children:
            json_product_child = JsonProductChild().parse_from_json(json_object_child)
            self.children.append(json_product_child)

        # Don't hand back an assembly if there are no children
        if len(self.children) > 0:
            return self
        else:
            return None

        def write_to_freecad(self, active_document):
            # This assembly may refer to a part as well
            # hence if there is a partUuid and if there is a part name, than
            # it should be written to the FreeCAD document as well.
            if self.is_part_reference():
                super().write_to_freecad(active_document)

            # And now write the children, they decide on their own if they reference
            # part or a product
            for child in self.children:
                child.write_to_freecad(active_document)
