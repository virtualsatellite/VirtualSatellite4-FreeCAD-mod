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


# TODO prints
class VirSatRestExporter():
    def exportFromDict(self, data_dict, api_instance, repo_name):
        root_product = data_dict[jd.JSON_PRODUCTS]
        parts = data_dict[jd.JSON_PARTS]

        try:
            # Read tree
            _, seis, _, visualisations = TreeCrawler().crawlTree(api_instance, repo_name)

            # TODO: already in crawler?
            # map uuid to sei
            # for json products in data_dict
            #   get the sei
            #   add to map of uuid -> existing elements

            # for part in data_dict
            for part in parts:
                # TODO: same as above, extract function?
                # update part:
                uuid = part[jd.JSON_ELEMENT_UUID]
                sei = seis[uuid]
                # TODO: nullcheck

                # get vis bean
                # TODO: function
                foundVisCa = None
                for ca_reference in sei.category_assignments:
                    if(ca_reference.uuid in visualisations.keys()):
                        foundVisCa = visualisations[ca_reference.uuid]
                print(foundVisCa)

                if foundVisCa is not None:
                    # update values from data dict
                    print(foundVisCa)
                    self.part2VisCa(part, foundVisCa)
                    print(foundVisCa)
                    # put vis bean again
                    # TODO: probably doesn't work this way
                    api_instance.put_ca(foundVisCa, repo_name, sync=False, _preload_content=False)
                else:
                    # TODO
                    pass

            # for product in data_dict
            self.exportProductsRecursive(root_product, seis, visualisations, api_instance, repo_name)
            api_instance.force_synchronize(repo_name)

        except Exception:
            print(traceback.format_exc())

    def exportProductsRecursive(self, product, seis, visualisations, api_instance, repo_name):
        # update product
        # TODO: has properties???
        # get vis bean
        print(product)
        uuid = product[jd.JSON_ELEMENT_UUID]
        sei = seis[uuid]
        # TODO: put doesn't work because type field is missing in swagger doc
        raw_sei = json.loads(api_instance.get_sei(uuid, repo_name, sync=False, _preload_content=False).data)
        # TODO: nullcheck

        # get vis bean
        # TODO: function
        foundVisCa = None
        for ca_reference in sei.category_assignments:
            if(ca_reference.uuid in visualisations.keys()):
                foundVisCa = visualisations[ca_reference.uuid]
        print(foundVisCa)

        if foundVisCa is not None:
            # update values from data dict
            foundVisCa["positionXBean"]["value"] = product[jd.JSON_ELEMENT_POS_X]
            foundVisCa["positionYBean"]["value"] = product[jd.JSON_ELEMENT_POS_Y]
            foundVisCa["positionZBean"]["value"] = product[jd.JSON_ELEMENT_POS_Z]
            foundVisCa["rotationXBean"]["value"] = product[jd.JSON_ELEMENT_ROT_X]
            foundVisCa["rotationYBean"]["value"] = product[jd.JSON_ELEMENT_ROT_Y]
            foundVisCa["rotationZBean"]["value"] = product[jd.JSON_ELEMENT_ROT_Z]
            raw_sei["name"] = product[jd.JSON_ELEMENT_NAME]

            # put vis bean and sei again
            api_instance.put_ca(foundVisCa, repo_name, sync=False, _preload_content=False)
            # api_instance.put_sei(sei, repo_name, sync=False)
            api_instance.put_sei(raw_sei, repo_name, sync=False, _preload_content=False)
        else:
            # TODO
            pass

        # Recursion
        for child_product in product[jd.JSON_ELEMNT_CHILDREN]:
            self.exportProductsRecursive(child_product, seis, visualisations, api_instance, repo_name)

    def part2VisCa(self, part, visCa):
        # For now assume correct units
        # For now ignore name changes
        visCa["shapeBean"]["value"] = part[jd.JSON_ELEMENT_SHAPE]
        visCa["colorBean"]["value"] = part[jd.JSON_ELEMENT_COLOR]
        visCa["sizeXBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_X]
        visCa["sizeYBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_Y]
        visCa["sizeZBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_Z]
        visCa["radiusBean"]["value"] = part[jd.JSON_ELEMENT_RADIUS]
