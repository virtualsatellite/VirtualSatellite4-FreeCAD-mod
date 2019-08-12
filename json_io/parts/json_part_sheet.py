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

FREECAD_PART_SHEET_NAME = "VirtualSatellitePart"


class JsonPartSheet(AJsonPart):

    def write_to_freecad(self, active_document):
        sheet = active_document.getObject(FREECAD_PART_SHEET_NAME)
        if sheet is None:
            sheet = active_document.addObject("Spreadsheet::Sheet", FREECAD_PART_SHEET_NAME)

        sheet.set("A1", "Virtual Satellite Part Data")
        sheet.set("A2", "Name")
        sheet.set("B2", "Value")
        sheet.set("C2", "Unit")
        sheet.setStyle("A1:C2", "bold")

        sheet_line = 3
        for json_part_attribute_name in list(self.attributes.keys()):

            json_part_attribute_value = str(getattr(self, json_part_attribute_name))
            json_part_attribute_unit = self.attributes[json_part_attribute_name]

            sheet.set("A" + str(sheet_line), json_part_attribute_name)
            sheet.set("B" + str(sheet_line), json_part_attribute_value)
            sheet.set("C" + str(sheet_line), json_part_attribute_unit)

            sheet_line += 1

    def read_sheet_attribute(self, active_document, attribute_name):
        sheet = active_document.getObject(FREECAD_PART_SHEET_NAME)
        column_a_cells = list(filter(lambda x: x.startswith('A'), sheet.PropertiesList))

        for a_cell in column_a_cells:
            if a_cell == attribute_name:
                b_cell = a_cell.replace("A", "B")
                return sheet.get(b_cell)
