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
import plugins.VirtualSatelliteRestPlugin.virsat_constants as vc
Err = FreeCAD.Console.PrintError
Log = FreeCAD.Console.PrintLog
Wrn = FreeCAD.Console.PrintWarning


class VirSatRestExporter():
    def exportFromDict(self, data_dict, api_instance, repo_name):
        root_product = data_dict[jd.JSON_PRODUCTS]
        parts = data_dict[jd.JSON_PARTS]

        try:
            # Read tree
            _, seis, _, visualisations = TreeCrawler().crawl_tree(api_instance, repo_name)

            for part in parts:
                uuid = part[jd.JSON_ELEMENT_UUID]
                name = part[jd.JSON_ELEMENT_NAME]
                part_id = name + '(' + uuid + ')'

                sei = seis[uuid]
                if sei is None:
                    Err('No sei found for part:{}\n'.format(part_id))
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
                    # In the future we could create a new one here
                    Wrn('{} not updated\n'.format(part_id))

            self.exportProductsRecursive(root_product, seis, visualisations, api_instance, repo_name)
            api_instance.force_synchronize(repo_name)

        except Exception:
            Err(traceback.format_exc())

    def exportProductsRecursive(self, product, seis, visualisations, api_instance, repo_name):
        uuid = product[jd.JSON_ELEMENT_UUID]
        name = product[jd.JSON_ELEMENT_NAME]
        product_id = name + '(' + uuid + ')'
        Log('Exporting product {}\n'.format(product_id))

        sei = seis[uuid]
        if sei is None:
            Err('No sei found for product: {}\n'.format(product_id))
            return None
        raw_sei = json.loads(api_instance.get_sei(uuid, repo_name, sync=False, _preload_content=False).data)

        foundVisCa = self.getVisCaForSei(sei, visualisations)

        if foundVisCa is not None:
            # Update values from data dict
            superVisCa = None
            if sei.super_seis:
                superVisCa = self.getVisCaForSei(seis[sei.super_seis[0].uuid], visualisations)
            self.product2VisCa(product, foundVisCa, superVisCa)
            raw_sei[vc.NAME] = product[jd.JSON_ELEMENT_NAME]

            # Put vis bean and sei again
            api_instance.put_ca(foundVisCa, repo_name, sync=False, _preload_content=False)
            api_instance.put_sei(raw_sei, repo_name, sync=False, _preload_content=False)
        else:
            # In the future we could create a new one here
            Wrn('No visualization for {} updated\n'.format(product_id))

        # Recursion
        for child_product in product[jd.JSON_ELEMNT_CHILDREN]:
            self.exportProductsRecursive(child_product, seis, visualisations, api_instance, repo_name)

    def part2VisCa(self, part, visCa, superCa):
        # For now assume correct units
        # For now ignore name changes
        # For now geometry files are not exported
        self.updateValueAndOverride(vc.SHAPE, part[jd.JSON_ELEMENT_SHAPE], visCa, superCa)
        self.updateValueAndOverride(vc.COLOR, part[jd.JSON_ELEMENT_COLOR], visCa, superCa)
        self.updateValueAndOverride(vc.SIZE_X, part[jd.JSON_ELEMENT_LENGTH_X], visCa, superCa)
        self.updateValueAndOverride(vc.SIZE_Y, part[jd.JSON_ELEMENT_LENGTH_Y], visCa, superCa)
        self.updateValueAndOverride(vc.SIZE_Z,  part[jd.JSON_ELEMENT_LENGTH_Z], visCa, superCa)
        self.updateValueAndOverride(vc.RADIUS, part[jd.JSON_ELEMENT_RADIUS], visCa, superCa)

    def product2VisCa(self, product, visCa, superCa):
        self.updateValueAndOverride(vc.POSITION_X, product[jd.JSON_ELEMENT_POS_X], visCa, superCa)
        self.updateValueAndOverride(vc.POSITION_Y, product[jd.JSON_ELEMENT_POS_Y], visCa, superCa)
        self.updateValueAndOverride(vc.POSITION_Z, product[jd.JSON_ELEMENT_POS_Z], visCa, superCa)
        self.updateValueAndOverride(vc.ROTATION_X, product[jd.JSON_ELEMENT_ROT_X], visCa, superCa)
        self.updateValueAndOverride(vc.ROTATION_Y, product[jd.JSON_ELEMENT_ROT_Y], visCa, superCa)
        self.updateValueAndOverride(vc.ROTATION_Z, product[jd.JSON_ELEMENT_ROT_Z], visCa, superCa)

    def updateValueAndOverride(self, beanName, newValue, visCa, superCa):
        # Set override if necessary
        if(superCa is not None):
            if(newValue != superCa[beanName][vc.VALUE]):
                visCa[beanName][vc.OVERRIDE] = True
            else:
                visCa[beanName][vc.OVERRIDE] = False

        # Set new value
        visCa[beanName][vc.VALUE] = newValue

    def getVisCaForSei(self, sei, visualisations):
        # Get visualization bean
        foundVisCa = None
        for ca_reference in sei.category_assignments:
            if(ca_reference.uuid in visualisations.keys()):
                foundVisCa = visualisations[ca_reference.uuid]
        return foundVisCa
