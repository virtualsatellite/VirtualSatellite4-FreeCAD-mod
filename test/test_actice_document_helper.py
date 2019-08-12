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


import FreeCAD
import FreeCADGui
from freecad.active_document_helper import ActiveDocumentHelper
import os
from test.test_setup import AWorkingDirectoryTest

App = FreeCAD
Gui = FreeCADGui


class TestActiveDocumentHelper(AWorkingDirectoryTest):

    @classmethod
    def setUpClass(cls):
        cls.setUpDirectory("ActiveDocumentHelper/")
        cls._WORKING_DIRECTORY = cls.getDirectoryFullPath()

    def tearDown(self):
        super().tearDown()

    def test_get_file_full_path(self):
        TEST_DOCUMENT_NAME = "box_263_456_789_111"

        file_full_path = ActiveDocumentHelper(self._WORKING_DIRECTORY).get_file_full_path(TEST_DOCUMENT_NAME)
        self.assertEqual(file_full_path, "/tmp/FreeCADtest/ActiveDocumentHelper/box_263_456_789_111.FCstd", "Got correct full path")

    def test_create_document(self):
        TEST_DOCUMENT_NAME = "box_263_456_789_222"

        loaded_documents = list(App.listDocuments().keys())
        self.assertNotIn(TEST_DOCUMENT_NAME, loaded_documents, "New Document is not yet loaded")

        active_document = ActiveDocumentHelper(self._WORKING_DIRECTORY).open_set_and_get_document(TEST_DOCUMENT_NAME)

        loaded_documents = list(App.listDocuments().keys())
        self.assertIn(TEST_DOCUMENT_NAME, loaded_documents, "Document is now loaded")

        self.assertIsNotNone(active_document, "Created a document")

    def test_save_and_close_active_document(self):
        TEST_DOCUMENT_NAME = "box_263_456_789_333"

        loaded_documents = list(App.listDocuments().keys())
        self.assertNotIn(TEST_DOCUMENT_NAME, loaded_documents, "New Document is not yet loaded")

        ActiveDocumentHelper(self._WORKING_DIRECTORY).open_set_and_get_document(TEST_DOCUMENT_NAME)

        file_full_path = ActiveDocumentHelper(self._WORKING_DIRECTORY).get_file_full_path(TEST_DOCUMENT_NAME)

        self.assertFalse(os.path.isfile(file_full_path), "File not yet saved")

        ActiveDocumentHelper(self._WORKING_DIRECTORY).save_and_close_active_document(TEST_DOCUMENT_NAME)

        self.assertTrue(os.path.isfile(file_full_path), "File got saved")

        loaded_documents = list(App.listDocuments().keys())
        self.assertNotIn(TEST_DOCUMENT_NAME, loaded_documents, "Document got closed")

    def test_reopen_document(self):
        TEST_DOCUMENT_NAME = "box_263_456_789_444"

        loaded_documents = list(App.listDocuments().keys())
        self.assertNotIn(TEST_DOCUMENT_NAME, loaded_documents, "New Document is not yet loaded")
        self.assertEquals(0, len(loaded_documents), "List of loaded documents is still empty")

        ActiveDocumentHelper(self._WORKING_DIRECTORY).open_set_and_get_document(TEST_DOCUMENT_NAME)

        loaded_documents = list(App.listDocuments().keys())
        self.assertIn(TEST_DOCUMENT_NAME, loaded_documents, "Document is now loaded")
        self.assertEquals(1, len(loaded_documents), "There is only one document loaded.")

        # Now save and load the document
        App.ActiveDocument.addObject("Part::Box", "BoxReopen")

        ActiveDocumentHelper(self._WORKING_DIRECTORY).save_and_close_active_document(TEST_DOCUMENT_NAME)

        loaded_documents = list(App.listDocuments().keys())
        self.assertNotIn(TEST_DOCUMENT_NAME, loaded_documents, "Document got closed")

        ActiveDocumentHelper(self._WORKING_DIRECTORY).open_set_and_get_document(TEST_DOCUMENT_NAME)
        freecad_object = App.ActiveDocument.getObject("BoxReopen")

        self.assertIsNotNone(freecad_object, "Was able to read file and get specific object for this test")

        # Call the method a second time and see that it is the same
        # therefore add an object and make sure it still exists after reopening
        App.ActiveDocument.addObject("Part::Box", "BoxReopen2")
        freecad_object = App.ActiveDocument.getObject("BoxReopen")

        loaded_documents = list(App.listDocuments().keys())
        self.assertEquals(1, len(loaded_documents), "Document is still loaded, just open it.")
        ActiveDocumentHelper(self._WORKING_DIRECTORY).open_set_and_get_document(TEST_DOCUMENT_NAME)
        loaded_documents = list(App.listDocuments().keys())
        self.assertEquals(1, len(loaded_documents), "Document is still the same. No other document got loaded.")

        freecad_object1 = App.ActiveDocument.getObject("BoxReopen")
        freecad_object2 = App.ActiveDocument.getObject("BoxReopen2")

        self.assertIsNotNone(freecad_object1, "Specific Object 1 exists")
        self.assertIsNotNone(freecad_object2, "Specific Object 2 did not disappear while reopening")
