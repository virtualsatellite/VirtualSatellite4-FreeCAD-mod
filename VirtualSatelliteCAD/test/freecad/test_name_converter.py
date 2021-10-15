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
import unittest
import freecad.name_converter as nc


class TestNameConverter(unittest.TestCase):

    TEST_NAME = "Many_Special-Characters Test.file"
    TEST_FREECAD_NAME = "Many__Special___Characters____Test_____file"

    def test_toFreeCad(self):
        assert(self.TEST_FREECAD_NAME, nc.toFreeCad(self.TEST_NAME))

    def test_fromFreeCad(self):
        assert(self.TEST_NAME, nc.fromFreeCad(self.TEST_FREECAD_NAME))

    def test_Roundtrip(self):
        assert(self.TEST_NAME, nc.fromFreeCad(nc.toFreeCad(self.TEST_NAME)))
        assert(self.TEST_FREECAD_NAME, nc.toFreeCad(nc.fromFreeCad(self.TEST_FREECAD_NAME)))
