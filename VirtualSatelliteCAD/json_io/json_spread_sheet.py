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

FREECAD_PART_SHEET_NAME = "VS"
FREECAD_PART_SHEET_ATTRIBUTE_START_LINE = 3


class JsonSpreadSheet(object):
    '''
    This class handles the io of the part properties to an excel sheet
    '''

    def __init__(self, json_part_or_product):
        self._json_part_or_product = json_part_or_product

    def create_sheet_name(self):
        return FREECAD_PART_SHEET_NAME + "_" + self._json_part_or_product.get_unique_name()

    def is_sheet_attached(self, active_document):
        sheet_name = self.create_sheet_name()
        sheet = active_document.app_active_document.getObject(sheet_name)
        sheet_attached = sheet is not None
        return sheet_attached

    def write_to_freecad(self, active_document):
        '''
        This method writes all part properties into an excel sheet
        within the part file. This sheet will be needed to read
        out the uuid of the part which corresponds to the uuid of
        virtual satellite.
        '''

        sheet_name = self.create_sheet_name()
        sheet = active_document.app_active_document.getObject(sheet_name)
        if not self.is_sheet_attached(active_document):
            sheet = active_document.app_active_document.addObject("Spreadsheet::Sheet", sheet_name)

        sheet.set("A1", "Virtual Satellite Part Data")
        sheet.set("A2", "Name")
        sheet.set("B2", "Value")
        sheet.set("C2", "Unit")
        sheet.setStyle("A1:C2", "bold")

        sheet_line = FREECAD_PART_SHEET_ATTRIBUTE_START_LINE
        for json_part_attribute_name in list(self._json_part_or_product.attributes.keys()):

            # TODO: added this try catch because some children would not have part_name and attribute (because they are assemblies)
            try:
                json_part_attribute_value = str(getattr(self._json_part_or_product, json_part_attribute_name))
                json_part_attribute_unit = self._json_part_or_product.attributes[json_part_attribute_name]

                sheet.set("A" + str(sheet_line), json_part_attribute_name)
                sheet.set("B" + str(sheet_line), json_part_attribute_value)
                sheet.set("C" + str(sheet_line), json_part_attribute_unit)

                sheet_line += 1
            except AttributeError as e:
                print(e)

        # Recompute the sheet, so that all properties are correctly written
        # if not recomputed accessing the properties will result in none objects
        active_document.app_active_document.recompute()

    def read_sheet_attribute(self, active_document, attribute_name):
        '''
        This method can be used to read from the part sheet from a
        given document. The method allows to individually access the
        written properties.
        '''
        sheet_name = self.create_sheet_name()
        sheet = active_document.app_active_document.getObject(sheet_name)
        attribute_index = list(self._json_part_or_product.attributes).index(attribute_name)

        if (attribute_index >= 0 and attribute_index < len(self._json_part_or_product.attributes)):
            return sheet.get("B" + str(attribute_index + FREECAD_PART_SHEET_ATTRIBUTE_START_LINE))
