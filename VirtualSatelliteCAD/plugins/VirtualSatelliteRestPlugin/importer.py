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

import json_io.json_definitions as jd
from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
import traceback


# TODO prints
class VirSatRestImporter():
    def importToDict(self, api_instance, repo_name, start_sei_name):
        try:
            # Read tree
            root_seis, seis, _, visualisations = TreeCrawler().crawlTree(api_instance, repo_name)
            seis2products = {}
            parts = []
            print(seis)
            print(_)
            print(visualisations)

            # Find the selected starting sei
            for sei in seis.values():
                if(sei.name == start_sei_name):

                    # Import starting at the sei
                    products = self.importRecursive(sei, root_seis, seis, visualisations, seis2products, parts)
                    if products is not None:
                        data_dict = {
                            jd.JSON_PRODUCTS: products,
                            jd.JSON_PARTS: parts
                        }
                        print(data_dict)
                        return data_dict

        except Exception:
            print(traceback.format_exc())
        return

    def importRecursive(self, sei, root_seis, seis, visualisations, seis2products, parts):

        print(sei.name)

        # Search visualisation
        foundVisCa = None
        for ca_reference in sei.category_assignments:
            if(ca_reference.uuid in visualisations.keys()):
                foundVisCa = visualisations[ca_reference.uuid]
        print(foundVisCa)

        # Create product
        isRoot = sei.uuid in root_seis.keys()
        if(isRoot or foundVisCa is not None):

            product_dict = {
                jd.JSON_ELEMENT_NAME: sei.name,
                jd.JSON_ELEMENT_UUID: sei.uuid,
                jd.JSON_ELEMNT_CHILDREN: []
            }

            seis2products[sei.uuid] = product_dict

            if(foundVisCa is not None):
                # Add pos and rot
                # For now assume default units
                product_dict[jd.JSON_ELEMENT_POS_X] = foundVisCa["positionXBean"]["value"]
                product_dict[jd.JSON_ELEMENT_POS_Y] = foundVisCa["positionYBean"]["value"]
                product_dict[jd.JSON_ELEMENT_POS_Z] = foundVisCa["positionZBean"]["value"]
                product_dict[jd.JSON_ELEMENT_ROT_X] = foundVisCa["rotationXBean"]["value"]
                product_dict[jd.JSON_ELEMENT_ROT_Y] = foundVisCa["rotationYBean"]["value"]
                product_dict[jd.JSON_ELEMENT_ROT_Z] = foundVisCa["rotationZBean"]["value"]

                # None shapes don't have a part
                if(foundVisCa["shapeBean"]["value"] != jd.JSON_ELEMENT_SHAPE_NONE):
                    # TODO: resolve inheritance -> find the correct part
                    # Resolve super seis
                    # Starting from the lowest sei (current)
                    # If there are any overrides -> use this one, else go a level above if possible
                    part = self.visCa2Part(foundVisCa, sei)
                    parts.append(part)
                    product_dict[jd.JSON_ELEMENT_PART_NAME] = part[jd.JSON_ELEMENT_NAME]
                    product_dict[jd.JSON_ELEMENT_PART_UUID] = part[jd.JSON_ELEMENT_UUID]

            if(sei.parent is not None):
                # The parent should already have been processed
                parentProduct = seis2products[sei.parent]
                parentProduct[jd.JSON_ELEMNT_CHILDREN].append(product_dict)

        # Recursion
        for child_refernce in sei.children:
            self.importRecursive(seis[child_refernce.uuid], root_seis, seis, visualisations, seis2products, parts)

        # Return for the initial call
        if parts:
            return seis2products[sei.uuid]
        else:
            return None

    def visCa2Part(self, visCa, containingSei):
        # For now assume correct units
        part_dict = {
            jd.JSON_ELEMENT_NAME: containingSei.name,
            jd.JSON_ELEMENT_UUID: containingSei.uuid,
            jd.JSON_ELEMENT_SHAPE: visCa["shapeBean"]["value"],
            jd.JSON_ELEMENT_COLOR: visCa["colorBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_X: visCa["sizeXBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_Y: visCa["sizeYBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_Z: visCa["sizeZBean"]["value"],
            jd.JSON_ELEMENT_RADIUS: visCa["radiusBean"]["value"]
        }

        return part_dict
