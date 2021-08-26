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


class ApiSwitch():
    API_VERSIONS = ["0.0.1"]

    def get_api(self, version):
        if(version == "0.0.1"):
            # Configure HTTP basic authorization: basic
            configuration = v0_0_1_client.Configuration()
            print(configuration.host)
            # TODO: parameter
            configuration.username = 'admin'
            configuration.password = 'secure'

            # create an instance of the API class
            return v0_0_1_client.DefaultApi(v0_0_1_client.ApiClient(configuration))
        else:
            return None
