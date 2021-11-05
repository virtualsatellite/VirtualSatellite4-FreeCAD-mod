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
import json
import plugins.VirtualSatelliteRestPlugin.virsat_constants as vc
from plugins.VirtualSatelliteRestPlugin.virsat_constants import TYPE_VIS


class TreeCrawler():
    '''
    This class crawls the Model tree via the API and returns an in memory representation to avoid duplicate calls
    '''

    def crawl_tree(self, api_instance, repo_name):
        # Result dicts mapping uuids to elements
        root_seis, seis, cas, visualisations = {}, {}, {}, {}

        def recurseChildren(sei, isRoot=False):
            if(isRoot):
                root_seis[sei.uuid] = sei
            seis[sei.uuid] = sei

            for ca_reference in sei.category_assignments:
                # Don't load the content in a model object because the swagger model doesn't know the available cas
                response = api_instance.get_ca(ca_reference.uuid, repo_name, sync=False, _preload_content=False)
                data = json.loads(response.data)
                ca_uuid = data[vc.UUID]

                cas[ca_uuid] = data
                if(data[vc.TYPE] == TYPE_VIS):
                    visualisations[ca_uuid] = data

            # Recursion
            for child_refernce in sei.children:
                child = api_instance.get_sei(child_refernce.uuid, repo_name, sync=False)
                recurseChildren(child)

        # Get root Seis and sync
        for root_sei in api_instance.get_root_seis(repo_name):
            recurseChildren(root_sei, isRoot=True)

        return (root_seis, seis, cas, visualisations)

    def crawl_raw_seis(self, api_instance, repo_name):
        # Result dicts mapping uuids to elements
        root_seis, seis = {}, {}

        def recurseChildren(sei, isRoot=False):
            if(isRoot):
                root_seis[sei[vc.UUID]] = sei
            seis[sei[vc.UUID]] = sei

            # Recursion
            for child_refernce in sei[vc.CHILDREN]:
                response = api_instance.get_sei(child_refernce[vc.UUID], repo_name, sync=False, _preload_content=False)
                child = json.loads(response.data)
                recurseChildren(child)

        # Get root Seis and sync
        for root_sei in api_instance.get_root_seis(repo_name):
            # Currently no type field if fetched over the root sei endpoint
            # Workaround: fetch the concrete sei again
            response = api_instance.get_sei(root_sei.uuid, repo_name, sync=False, _preload_content=False)
            recurseChildren(json.loads(response.data), isRoot=True)

        return (root_seis, seis)
