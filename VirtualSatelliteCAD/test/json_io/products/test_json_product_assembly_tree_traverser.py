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
from test.test_setup import AWorkingDirectoryTest
from test.json_io.test_json_data import TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD, TEST_JSON_PRODUCT_WITHOUT_CHILDREN
import json
from json_io.products.json_product_assembly_tree_traverser import JsonProductAssemblyTreeTraverser
from json_io.json_definitions import JSON_ELEMNT_CHILDREN, JSON_ELEMENT_NAME
from json_io.products.json_product_assembly import JsonProductAssembly
from freecad.active_document import ActiveDocument


class TestJsonProductAssemblyTreeTraverser(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ProductAssemblyTreeTraverser/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_traverse_json(self):
        json_data = TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD
        self.create_Test_Part()

        json_object = json.loads(json_data)

        traverser = JsonProductAssemblyTreeTraverser(self._WORKING_DIRECTORY)
        traverser.traverse(json_object)
        lst_of_depths = traverser._lst_of_depths

        self.assertEqual(len(lst_of_depths), 2, "Found the right amount of 2 depths")
        self.assertEqual(len(lst_of_depths[0]), 1, "Found the right amount of 1 assembly at depth 0")
        self.assertEqual(len(lst_of_depths[1]), 1, "Found the right amount of 1 assembly at depth 1")
        self.assertEqual(lst_of_depths[0][0][JSON_ELEMENT_NAME], "BasePlateBottom1", "Found the right element at depth 0")
        self.assertEqual(lst_of_depths[1][0][JSON_ELEMENT_NAME], "BasePlateBottom2", "Found the right element at depth 1")

    def test_parse_json_from_tree_without_traversing(self):

        traverser = JsonProductAssemblyTreeTraverser(self._WORKING_DIRECTORY)
        self.assertIsNone(traverser.parse_from_json(), "Parsing no read in json object will result in 'None'")

    def test_traverse_and_parse_json_tree(self):
        json_data = TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD
        self.create_Test_Part()

        json_object = json.loads(json_data)

        traverser = JsonProductAssemblyTreeTraverser(self._WORKING_DIRECTORY)
        traverser.traverse(json_object)
        lst_of_depths = traverser._lst_of_depths

        self.assertEqual(len(lst_of_depths), 2, "Found the right amount of 2 assemblies")

        traverser.parse_from_json()

        # this should have similar results to test_create_part_product_assembly_and_subassembly_with_root_part_manual in TestJsonProductAssembly
        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("BasePlateBottom2_e8794f3d_86ec_44c5_9618_8b7170c45484")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 4, "Found correct amount of root objects 2 objects plus 2 sheets")

        active_document = ActiveDocument(self._WORKING_DIRECTORY).open_set_and_get_document("BasePlateBottom1_e8794f3d_86ec_44c5_9618_8b7170c45484")
        self.assertEquals(len(active_document.app_active_document.RootObjects), 6, "Found correct amount of root objects 3 objects plus 3 sheets")

    def test_traverse_and_parse_json_tree_rootassembly_without_children(self):
        json_data = TEST_JSON_PRODUCT_WITHOUT_CHILDREN
        self.create_Test_Part()

        json_object = json.loads(json_data)

        traverser = JsonProductAssemblyTreeTraverser(self._WORKING_DIRECTORY)
        traverser.traverse_and_parse_from_json(json_object)

        self.assertIsNone(traverser.parse_from_json())
