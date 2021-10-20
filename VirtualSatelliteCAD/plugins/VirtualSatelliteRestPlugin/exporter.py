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
import json
import FreeCAD
Err = FreeCAD.Console.PrintError
# TODO: log messages, extract constants
Log = FreeCAD.Console.PrintLog


class VirSatRestExporter():
    def exportFromDict(self, data_dict, api_instance, repo_name):
        root_product = data_dict[jd.JSON_PRODUCTS]
        parts = data_dict[jd.JSON_PARTS]

        try:
            # Read tree
            _, seis, _, visualisations = TreeCrawler().crawlTree(api_instance, repo_name)

            for part in parts:
                uuid = part[jd.JSON_ELEMENT_UUID]
                sei = seis[uuid]
                if sei is None:
                    Err('No sei found for part:' + part[jd.JSON_ELEMENT_NAME] + '(' + part[jd.JSON_ELEMENT_UUID] + ')')
                    return None

                foundVisCa = self.getVisCaForSei(sei, visualisations)

                if foundVisCa is not None:
                    # Update values from data dict
                    superVisCa = None
                    if sei.super_seis:
                        superVisCa = self.getVisCaForSei(seis[sei.super_seis[0].uuid], visualisations)
                    self.part2VisCa(part, foundVisCa, superVisCa)
                    # Put vis bean again
                    api_instance.put_ca(foundVisCa, repo_name, sync=False, _preload_content=False)
                else:
                    # TODO: create?
                    pass

            self.exportProductsRecursive(root_product, seis, visualisations, api_instance, repo_name)
            api_instance.force_synchronize(repo_name)

        except Exception:
            Err(traceback.format_exc())

    def exportProductsRecursive(self, product, seis, visualisations, api_instance, repo_name):
        uuid = product[jd.JSON_ELEMENT_UUID]
        sei = seis[uuid]
        if sei is None:
            Err('No sei found for product:' + product[jd.JSON_ELEMENT_NAME] + '(' + product[jd.JSON_ELEMENT_UUID] + ')')
            return None
        raw_sei = json.loads(api_instance.get_sei(uuid, repo_name, sync=False, _preload_content=False).data)

        foundVisCa = self.getVisCaForSei(sei, visualisations)

        if foundVisCa is not None:
            # Update values from data dict
            superVisCa = None
            if sei.super_seis:
                superVisCa = self.getVisCaForSei(seis[sei.super_seis[0].uuid], visualisations)
            self.product2VisCa(product, foundVisCa, superVisCa)
            raw_sei["name"] = product[jd.JSON_ELEMENT_NAME]

            # Put vis bean and sei again
            api_instance.put_ca(foundVisCa, repo_name, sync=False, _preload_content=False)
            api_instance.put_sei(raw_sei, repo_name, sync=False, _preload_content=False)
        else:
            # TODO: create?
            pass

        # Recursion
        for child_product in product[jd.JSON_ELEMNT_CHILDREN]:
            self.exportProductsRecursive(child_product, seis, visualisations, api_instance, repo_name)

    def part2VisCa(self, part, visCa, superCa):
        # For now assume correct units
        # For now ignore name changes
        # For now geometry files are not exported
        self.updateValueAndOverride("shapeBean", part[jd.JSON_ELEMENT_SHAPE], visCa, superCa)
        self.updateValueAndOverride("colorBean", part[jd.JSON_ELEMENT_COLOR], visCa, superCa)
        self.updateValueAndOverride("sizeXBean", part[jd.JSON_ELEMENT_LENGTH_X], visCa, superCa)
        self.updateValueAndOverride("sizeYBean", part[jd.JSON_ELEMENT_LENGTH_Y], visCa, superCa)
        self.updateValueAndOverride("sizeZBean",  part[jd.JSON_ELEMENT_LENGTH_Z], visCa, superCa)
        self.updateValueAndOverride("radiusBean", part[jd.JSON_ELEMENT_RADIUS], visCa, superCa)

    def product2VisCa(self, product, visCa, superCa):
        self.updateValueAndOverride("positionXBean", product[jd.JSON_ELEMENT_POS_X], visCa, superCa)
        self.updateValueAndOverride("positionYBean", product[jd.JSON_ELEMENT_POS_Y], visCa, superCa)
        self.updateValueAndOverride("positionZBean", product[jd.JSON_ELEMENT_POS_Z], visCa, superCa)
        self.updateValueAndOverride("rotationXBean", product[jd.JSON_ELEMENT_ROT_X], visCa, superCa)
        self.updateValueAndOverride("rotationYBean", product[jd.JSON_ELEMENT_ROT_Y], visCa, superCa)
        self.updateValueAndOverride("rotationZBean", product[jd.JSON_ELEMENT_ROT_Z], visCa, superCa)

    def updateValueAndOverride(self, beanName, newValue, visCa, superCa):
        # Set override if necessary
        Log(beanName)
        Log(newValue)
        if(superCa is not None):
            Log("Not none")
            Log(superCa["name"])
            Log(superCa[beanName]["value"])
        if(superCa is not None and newValue != superCa[beanName]["value"]):
            visCa[beanName]["override"] = True
            Log("Do override")
        # else:
        #    visCa[beanName]["override"] = False

        # Set new value
        visCa[beanName]["value"] = newValue

    def getVisCaForSei(self, sei, visualisations):
        # Get visualization bean
        foundVisCa = None
        for ca_reference in sei.category_assignments:
            if(ca_reference.uuid in visualisations.keys()):
                foundVisCa = visualisations[ca_reference.uuid]
        return foundVisCa
