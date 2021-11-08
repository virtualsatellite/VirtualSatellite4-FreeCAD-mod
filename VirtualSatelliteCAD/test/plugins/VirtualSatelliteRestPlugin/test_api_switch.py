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
import unittest
from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch


class TestApiSwitch(unittest.TestCase):

    def test_get_api(self):
        switch = ApiSwitch()
        host, username, password = 'host', 'username', 'password'

        self.assertEqual(switch.get_api(None, '', '', ''), None, "No API returned")
        self.assertEqual(switch.get_api(-1, '', '', ''), None, "No API returned")

        api = switch.get_api(0, host, username, password)
        self.assertEqual(
            "{0}.{1}".format(api.__class__.__module__, api.__class__.__name__),
            "plugins.VirtualSatelliteRestPlugin.generated_api.v0_0_1.swagger_client.api.default_api.DefaultApi",
            "Correct API returned")
        conf = api.api_client.configuration
        # Assert correct configuration
        self.assertTrue(host in conf.host)
        self.assertEqual(conf.username, username)
        self.assertEqual(conf.password, password)
