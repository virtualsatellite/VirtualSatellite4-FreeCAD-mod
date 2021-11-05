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
from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
from test.plugins.VirtualSatelliteRestPlugin.api_mocks import get_mock_api,\
    ROOT_SEI_EMPTY, COMPLEX_ROOT_SEIS,\
    SEI_VIS, ROOT_SEI_COMPLEX, CA_VIS_RESPONSE, CA_VIS, ROOT_SEI_CAS,\
    CA_NO_VIS, CA_NO_VIS_RESPONSE, ROOT_SEI_CA, ROOT_SEI_CHILD, SEI_EMPTY


class TestTreeCrawler(unittest.TestCase):

    def test_crawl_tree(self):
        crawler = TreeCrawler()
        mock_api = get_mock_api()

        # Test crawl tree with single root sei
        mock_api.get_root_seis.return_value = [ROOT_SEI_EMPTY]
        root_seis, _, _, _ = crawler.crawl_tree(mock_api, '')
        self.assertTrue(ROOT_SEI_EMPTY.uuid in root_seis)

        # Test crawl tree with  multiple root seis and child sei
        mock_api.get_root_seis.return_value = [ROOT_SEI_EMPTY, ROOT_SEI_CHILD]
        mock_api.get_sei.return_value = SEI_EMPTY
        root_seis, seis, _, _ = crawler.crawl_tree(mock_api, '')
        self.assertListEqual([*root_seis.keys()], [ROOT_SEI_EMPTY.uuid, ROOT_SEI_CHILD.uuid])
        self.assertListEqual([*seis.keys()], [ROOT_SEI_EMPTY.uuid, ROOT_SEI_CHILD.uuid, SEI_EMPTY.uuid])

        # Test crawl tree with single ca
        mock_api.get_root_seis.return_value = [ROOT_SEI_CA]
        # For raw cas we return the raw JSON data
        mock_api.get_ca.return_value = CA_NO_VIS_RESPONSE
        _, _, cas, visualisations = crawler.crawl_tree(mock_api, '')
        self.assertListEqual([*cas.keys()], [CA_NO_VIS.uuid])
        self.assertFalse(visualisations, "Dict is empty")

        # Test crawl tree with multiple cas
        mock_api.get_root_seis.return_value = [ROOT_SEI_CAS]
        # For raw cas we return the raw JSON data
        mock_api.get_ca.side_effect = [CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE]
        _, _, cas, visualisations = crawler.crawl_tree(mock_api, '')
        self.assertListEqual([*cas.keys()], [CA_VIS.uuid, CA_NO_VIS.uuid])
        self.assertListEqual([*visualisations.keys()], [CA_VIS.uuid])

        # Complex test case
        mock_api.get_root_seis.return_value = COMPLEX_ROOT_SEIS
        mock_api.get_sei.side_effect = [SEI_EMPTY, SEI_VIS]
        mock_api.get_ca.side_effect = [CA_VIS_RESPONSE, CA_NO_VIS_RESPONSE]
        root_seis, seis, cas, visualisations = crawler.crawl_tree(mock_api, '')
        self.assertListEqual([*root_seis.keys()], [ROOT_SEI_COMPLEX.uuid, ROOT_SEI_EMPTY.uuid])
        self.assertListEqual([*seis.keys()], [ROOT_SEI_COMPLEX.uuid, SEI_EMPTY.uuid, SEI_VIS.uuid, ROOT_SEI_EMPTY.uuid])
        self.assertListEqual([*cas.keys()], [CA_VIS.uuid, CA_NO_VIS.uuid])
        self.assertListEqual([*visualisations.keys()], [CA_VIS.uuid])
