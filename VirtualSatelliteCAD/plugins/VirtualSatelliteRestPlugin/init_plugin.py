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
    def importToDict(self):
        import json_io.json_definitions as jd

        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch
        # TODO: global
        api_instance = ApiSwitch().get_api("0.0.1")

        # TODO: preferences
        # TODO: select starting sei via dialog / preferences?
        # TODO: look export dialog: only product trees???
        repo_name = 'visDemo'

        # TOOD: reverse engineer virsat cad exporter
        try:
            # Get root Seis
            root_seis = api_instance.get_root_seis(repo_name)
            seis2products = {}
            parts = []
            for root_sei in root_seis:
                # TODO param
                if(root_sei.name == "ConfigurationTree"):
                    products = self.recurseChildren(root_sei, api_instance, repo_name, seis2products, parts, isRoot=True)
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

    def recurseChildren(self, sei, api_instance, repo_name, seis2products, parts, isRoot=False):
        import json
        import json_io.json_definitions as jd

        print(sei.name)
        # Search visualisation

        foundVisCa = None
        for ca_reference in sei.category_assignments:

            # Don't load the content in a model object because the swagger model doesn't know the available cas
            response = api_instance.get_ca(ca_reference.uuid, repo_name, sync=False, _preload_content=False)
            data = json.loads(response.data)
            if(data['type'] == 'visualisation'):
                foundVisCa = data

        # Create product
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
                    # TODO: resolve inheritance
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
            child = api_instance.get_sei(child_refernce.uuid, repo_name, sync=False)
            self.recurseChildren(child, api_instance, repo_name, seis2products, parts)

        # Return for the initial call
        if parts:
            return seis2products[sei.uuid]
        else:
            return None

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

    def exportFromDict(self, data_dict):
        # TOOD: reverse engineer virsat cad importer
        return


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
