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
import FreeCAD
import os
import sys

APPDATA_DIR = os.path.join(FreeCAD.ConfigGet("UserAppData"), "Mod", "VirtualSatelliteCAD")

# FreeCAD seems to load modules differently once they are stored in the User Home directory.
# We try to load the whole folder if it exists
freecad_user_home = FreeCAD.getUserAppDataDir()
freecad_user_mod = freecad_user_home + "Mod"

Log = FreeCAD.Console.PrintLog

Log("See if the directory " + freecad_user_mod + "exists...")

if os.path.isdir(freecad_user_mod):
    Log("Directory Exists... Check if it is already on the path...")
    if (freecad_user_mod in sys.path):
        Log("Directory is already on the path...")
    else:
        Log("Directory will be appended to system path...")
        sys.path.append(freecad_user_mod)

# Create an appdata directory
if not os.path.isdir(APPDATA_DIR):
    os.mkdir(APPDATA_DIR)

# Finally register the unit test for being executed with all other FreeCAD tests
FreeCAD.__unit_test__ += ["TestVirtualSatelliteApp"]
