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
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin


@Plugin.register
class VirSatPlugin(Plugin):
    '''
    Plugin that connects to a Virtual Satellite Server
    '''
    # TODO: extract classes for im- and export
    # TODO: test

    def importToDict(self):
        import json_io.json_definitions as jd
        from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch
        api_instance = ApiSwitch().get_api("0.0.1")  # TODO: preferences
        # TODO: select starting sei via dialog / preferences?
        # TODO: look export dialog: only product trees???
        repo_name = 'visDemo'

        # TOOD: reverse engineer virsat cad exporter
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
                # TODO: param
                if(sei.name == "ConfigurationTree"):

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
            import traceback
            print(traceback.format_exc())
        return

    def importRecursive(self, sei, root_seis, seis, visualisations, seis2products, parts):
        import json_io.json_definitions as jd

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

    # TODO extract helper
    def visCa2Part(self, visCa, containingSei):
        import json_io.json_definitions as jd
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

    def part2VisCa(self, part, visCa):
        import json_io.json_definitions as jd
        # For now assume correct units
        # For now ignore name changes
        visCa["shapeBean"]["value"] = part[jd.JSON_ELEMENT_SHAPE]
        visCa["colorBean"]["value"] = part[jd.JSON_ELEMENT_COLOR]
        visCa["sizeXBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_X]
        visCa["sizeYBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_Y]
        visCa["sizeZBean"]["value"] = part[jd.JSON_ELEMENT_LENGTH_Z]
        visCa["radiusBean"]["value"] = part[jd.JSON_ELEMENT_RADIUS]

    def exportFromDict(self, data_dict):
        import json_io.json_definitions as jd
        from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch
        api_instance = ApiSwitch().get_api("0.0.1")  # TODO: preferences
        # TODO: select starting sei via dialog / preferences?
        # TODO: look export dialog: only product trees???
        repo_name = 'visDemo'
        # TOOD: reverse engineer virsat cad importer

        print(data_dict)
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
            import traceback
            print(traceback.format_exc())
        return

    def exportProductsRecursive(self, product, seis, visualisations, api_instance, repo_name):
        import json_io.json_definitions as jd
        import json
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


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
