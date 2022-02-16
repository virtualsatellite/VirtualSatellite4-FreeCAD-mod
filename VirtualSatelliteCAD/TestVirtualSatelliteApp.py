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

from test.json_io.test_json_importer import TestJsonImporter  # NOQA 
from test.json_io.test_json_exporter import TestJsonExporter # NOQA 
from test.json_io.test_json_spread_sheet import TestJsonSpreadSheet # NOQA
from test.json_io.parts.test_json_part import TestJsonPart  # NOQA 
from test.json_io.parts.test_json_part_box import TestJsonPartBox  # NOQA 
from test.json_io.parts.test_json_part_cone import TestJsonPartCone  # NOQA 
from test.json_io.parts.test_json_part_cylinder import TestJsonPartCylinder  # NOQA 
from test.json_io.parts.test_json_part_sphere import TestJsonPartSphere  # NOQA 
from test.json_io.parts.test_json_part_geometry import TestJsonPartGeometry  # NOQA 
from test.json_io.parts.test_json_part_factory import TestJsonPartFactory # NOQA
from test.json_io.products.test_json_product import TestJsonProduct # NOQA
from test.json_io.products.test_json_product_assembly import TestJsonProductAssembly # NOQA
from test.json_io.products.test_json_product_child import TestJsonProductChild # NOQA
from test.json_io.products.test_json_product_assembly_tree_traverser import TestJsonProductAssemblyTreeTraverser # NOQA
from test.freecad.test_actice_document import TestActiveDocument # NOQA
from test.plugins.VirtualSatelliteRestPlugin.test_api_switch import TestApiSwitch # NOQA
from test.plugins.VirtualSatelliteRestPlugin.test_tree_crawler import TestTreeCrawler # NOQA
from test.plugins.VirtualSatelliteRestPlugin.test_importer import TestImporter # NOQA
from test.plugins.VirtualSatelliteRestPlugin.test_exporter import TestExorter # NOQA
from test.freecad.test_name_converter import TestNameConverter # NOQA
from test.scripts.thermal.test_prepare_model import TestPrepareModel # NOQA
