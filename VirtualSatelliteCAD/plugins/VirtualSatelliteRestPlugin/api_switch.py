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
import plugins.VirtualSatelliteRestPlugin.generated_api.v0_0_1.swagger_client as v0_0_1_client
import FreeCAD
Msg = FreeCAD.Console.PrintMessage

API_VERSIONS = {
    0: "0.0.1"
}


class ApiSwitch():

    def get_api(self, version_idx, host, username, password):
        # Identifier is the index from the preferences
        # Because combo boxes only save their selected index
        version = API_VERSIONS.get(version_idx, "Unknown Index")

        if(version == "0.0.1"):
            # Configure HTTP basic authorization: basic
            configuration = v0_0_1_client.Configuration()
            api_host = host + "/rest/model/v" + version
            configuration.host = api_host
            configuration.username = username
            configuration.password = password

            Msg('Creating API of version:"{}" for "{}"\n'.format(version, api_host))
            # Create an instance of the API class
            return v0_0_1_client.DefaultApi(v0_0_1_client.ApiClient(configuration))

        Msg('API version:"{}" not supported\n'.format(version))
        return None
