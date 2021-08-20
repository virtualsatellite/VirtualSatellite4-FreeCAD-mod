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

        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch
        api_instance = ApiSwitch().get_api("0.0.1")

        # TODO: preferences
        repo_name = 'visDemo'
        sync = True
        build = True

        # TOOD: reverse engineer virsat cad exporter
        try:
            # Get root Seis
            data = api_instance.get_root_seis(repo_name, sync=sync, build=build)
            print(data)
            print(data[0])
            print(data[0].name)
        except Exception as e:
            print("Exception when calling DefaultApi->get_root_seis: %s\n" % e)
        return

    def exportFromDict(self, data_dict):
        return


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
