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


class JsonProductChild(AJsonProduct):
    pass

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
