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


"""
As FreeCAD only supports alphanumerical and _ (underscore) in it's names,
this class provides utility to convert names containing special characters into the FreeCAD form and back.
It works as long as no name contains concatenated underscores
"""


def toFreeCad(name):
    # As _ is reserved as a delimiter it will also be replaced
    name = name.replace("_", "__")
    name = name.replace("-", "___")
    name = name.replace(" ", "____")
    name = name.replace(".", "_____")

    return name


def fromFreeCad(name):
    name = name.replace("_____", ".")
    name = name.replace("____", " ")
    name = name.replace("___", "-")
    name = name.replace("__", "_")

    return name
