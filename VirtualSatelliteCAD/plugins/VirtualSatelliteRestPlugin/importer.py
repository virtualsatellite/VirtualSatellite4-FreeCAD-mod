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
import FreeCAD
Err = FreeCAD.Console.PrintError
# TODO: log messages
Log = FreeCAD.Console.PrintLog


class VirSatRestImporter():
    def __init__(self, project_directory, api_instance, repo_name):
        self.project_directory, self.api_instance, self.repo_name = project_directory, api_instance, repo_name

    def importToDict(self, start_sei_uuid):
        try:
            # Read tree
            root_seis, seis, _, visualisations = TreeCrawler().crawlTree(self.api_instance, self.repo_name)
            seis2products = {}
            parts = []

            # Find the selected starting sei
            for sei in seis.values():
                if(sei.uuid == start_sei_uuid):

                    # Import starting at the sei
                    products = self.importRecursive(sei, root_seis, seis, visualisations, seis2products, parts)
                    if products is not None:
                        data_dict = {
                            jd.JSON_PRODUCTS: products,
                            jd.JSON_PARTS: parts
                        }
                        return data_dict

        except Exception:
            Err(traceback.format_exc())
        return

    def importRecursive(self, sei, root_seis, seis, visualisations, seis2products, parts):

        # Search visualisation
        foundVisCa = self.getVisCaForSei(sei, visualisations)

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
                    # Resolve inheritance -> find the correct part
                    partVis, partSei = self.resolveInheritance(foundVisCa, sei, visualisations, seis)
                    Log(partVis)
                    part = self.visCa2Part(partVis, partSei)
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

    def getVisCaForSei(self, sei, visualisations):
        # Get visualization bean
        foundVisCa = None
        for ca_reference in sei.category_assignments:
            if(ca_reference.uuid in visualisations.keys()):
                foundVisCa = visualisations[ca_reference.uuid]
        return foundVisCa

    def visCa2Part(self, visCa, containingSei):
        import os
        # For now assume correct units
        shape = visCa["shapeBean"]["value"]

        part_dict = {
            jd.JSON_ELEMENT_NAME: containingSei.name,
            jd.JSON_ELEMENT_UUID: containingSei.uuid,
            jd.JSON_ELEMENT_SHAPE: shape,
            jd.JSON_ELEMENT_COLOR: visCa["colorBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_X: visCa["sizeXBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_Y: visCa["sizeYBean"]["value"],
            jd.JSON_ELEMENT_LENGTH_Z: visCa["sizeZBean"]["value"],
            jd.JSON_ELEMENT_RADIUS: visCa["radiusBean"]["value"],
        }

        geometryFilePath = visCa["geometryFileBean"]["value"]
        if(shape == jd.JSON_ELEMENT_SHAPE_GEOMETRY):
            # Download the STL file from the server
            response = self.api_instance.get_resource(visCa["geometryFileBean"]["uuid"], self.repo_name, sync=False, _preload_content=False)
            local_path = os.path.join(self.project_directory, containingSei.uuid.replace('-', '_') + '.' + geometryFilePath.split('/')[-1])
            f = open(local_path, 'wb')
            f.write(response.data)
            f.close()
            part_dict[jd.JSON_ELEMENT_STL_PATH] = local_path

        return part_dict

    # TODO: cpmplex test
    def resolveInheritance(self, visCa, containingSei, visualisations, seis):
        partVis, partSei = visCa, containingSei

        # Starting from the lowest sei (current) check if found vis has any overrides
        while(partVis is not None and not self.overridesAnyPartValue(partVis)):
            nextPartVis, nextPartSei = None, partSei

            # If there were no overrides we can step upwards in the inheritance tree
            # Until we find the next visualisation
            while(nextPartSei.parent is not None and nextPartVis is None):
                nextPartSei = seis[nextPartSei.parent]
                nextPartVis = self.getVisCaForSei(nextPartSei, visualisations)

            # Possibly we didn't find any visualisation in the complete inheritance tree
            # Then we keep the current one
            if nextPartVis is not None:
                partVis, partSei = nextPartVis, nextPartSei

            # Abort if inheritance tree is exhausted
            if(nextPartSei.parent is None):
                break

        return (partVis, partSei)

    def overridesAnyPartValue(self, visCa):
        (
            visCa["shapeBean"]["override"] or
            visCa["colorBean"]["override"] or
            visCa["sizeXBean"]["override"] or
            visCa["sizeYBean"]["override"] or
            visCa["sizeZBean"]["override"] or
            visCa["radiusBean"]["override"] or
            visCa["geometryFileBean"]["override"]
        )
