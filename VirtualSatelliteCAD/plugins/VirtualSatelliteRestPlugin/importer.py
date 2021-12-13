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
import plugins.VirtualSatelliteRestPlugin.virsat_constants as vc
import freecad.name_converter as nc
from plugins.VirtualSatelliteRestPlugin.api_kinds import PROPERTIES
Err = FreeCAD.Console.PrintError
Log = FreeCAD.Console.PrintLog
Wrn = FreeCAD.Console.PrintWarning


class VirSatRestImporter():
    def __init__(self, project_directory, api_instances, repo_name):
        self.project_directory, self.api_instances, self.repo_name = project_directory, api_instances, repo_name

    def importToDict(self, start_sei_uuid):
        Log('Calling import in Virtual Satellite REST importer\n')
        try:
            # Read tree
            root_seis, seis, _, visualisations = TreeCrawler().crawl_tree(self.api_instances, self.repo_name)
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
        sei_id = sei.name + '(' + sei.uuid + ')'
        Log('Importing sei {}\n'.format(sei_id))

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
                product_dict[jd.JSON_ELEMENT_POS_X] = foundVisCa[vc.POSITION_X][vc.VALUE]
                product_dict[jd.JSON_ELEMENT_POS_Y] = foundVisCa[vc.POSITION_Y][vc.VALUE]
                product_dict[jd.JSON_ELEMENT_POS_Z] = foundVisCa[vc.POSITION_Z][vc.VALUE]
                product_dict[jd.JSON_ELEMENT_ROT_X] = foundVisCa[vc.ROTATION_X][vc.VALUE]
                product_dict[jd.JSON_ELEMENT_ROT_Y] = foundVisCa[vc.ROTATION_Y][vc.VALUE]
                product_dict[jd.JSON_ELEMENT_ROT_Z] = foundVisCa[vc.ROTATION_Z][vc.VALUE]

                # None shapes don't have a part
                if(foundVisCa[vc.SHAPE][vc.VALUE] != jd.JSON_ELEMENT_SHAPE_NONE):
                    # Resolve inheritance -> find the correct part
                    partVis, partSei = self.resolveVisInheritance(foundVisCa, sei, visualisations, seis)
                    part = self.visCa2Part(partVis, partSei)
                    parts.append(part)
                    product_dict[jd.JSON_ELEMENT_PART_NAME] = part[jd.JSON_ELEMENT_NAME]
                    product_dict[jd.JSON_ELEMENT_PART_UUID] = part[jd.JSON_ELEMENT_UUID]

            if(sei.parent is not None):
                if(sei.parent in seis2products):
                    # The parent should already have been processed
                    parentProduct = seis2products[sei.parent]
                    parentProduct[jd.JSON_ELEMNT_CHILDREN].append(product_dict)
                else:
                    # If a non root sei was selected as starting sei, a parent may not be known (not in the subtree)
                    # Or there is no product because it has no visualization, so try to resolve the parents
                    resolvedParentProduct = self.searchParentWithProduct(sei, seis, seis2products)
                    if(resolvedParentProduct is not None):
                        resolvedParentProduct[jd.JSON_ELEMNT_CHILDREN].append(product_dict)
                    else:
                        Wrn('No parent product found for {}\n'.format(sei_id))

        # Recursion
        for child_refernce in sei.children:
            self.importRecursive(seis[child_refernce.uuid], root_seis, seis, visualisations, seis2products, parts)

        # Return for the initial call
        if parts and sei.uuid in seis2products:
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
        shape = visCa[vc.SHAPE][vc.VALUE]

        part_dict = {
            jd.JSON_ELEMENT_NAME: containingSei.name,
            jd.JSON_ELEMENT_UUID: containingSei.uuid,
            jd.JSON_ELEMENT_SHAPE: shape,
            jd.JSON_ELEMENT_COLOR: visCa[vc.COLOR][vc.VALUE],
            jd.JSON_ELEMENT_LENGTH_X: visCa[vc.SIZE_X][vc.VALUE],
            jd.JSON_ELEMENT_LENGTH_Y: visCa[vc.SIZE_Y][vc.VALUE],
            jd.JSON_ELEMENT_LENGTH_Z: visCa[vc.SIZE_Z][vc.VALUE],
            jd.JSON_ELEMENT_RADIUS: visCa[vc.RADIUS][vc.VALUE],
        }

        geometryFilePath = visCa[vc.GEOMETRY][vc.VALUE]
        if(shape == jd.JSON_ELEMENT_SHAPE_GEOMETRY):
            # Download the STL file from the server
            response = self.api_instances[PROPERTIES].get_resource(visCa[vc.GEOMETRY][vc.UUID], self.repo_name, sync=False, _preload_content=False)
            local_path = os.path.join(self.project_directory, nc.toFreeCad(containingSei.uuid) + '.' + geometryFilePath.split('/')[-1])
            f = open(local_path, 'wb')
            f.write(response.data)
            f.close()
            part_dict[jd.JSON_ELEMENT_STL_PATH] = local_path

        return part_dict

    def resolveVisInheritance(self, visCa, containingSei, visualisations, seis):
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

    def searchParentWithProduct(self, sei, seis, seis2products):
        nextSei = sei

        while(nextSei.parent is not None):
            parent_uuid = nextSei.parent

            if(parent_uuid in seis2products):
                return seis2products[parent_uuid]

            nextSei = seis[parent_uuid]

        return

    def overridesAnyPartValue(self, visCa):
        (
            visCa[vc.SHAPE][vc.OVERRIDE] or
            visCa[vc.COLOR][vc.OVERRIDE] or
            visCa[vc.SIZE_X][vc.OVERRIDE] or
            visCa[vc.SIZE_Y][vc.OVERRIDE] or
            visCa[vc.SIZE_Z][vc.OVERRIDE] or
            visCa[vc.RADIUS][vc.OVERRIDE] or
            visCa[vc.GEOMETRY][vc.OVERRIDE]
        )
