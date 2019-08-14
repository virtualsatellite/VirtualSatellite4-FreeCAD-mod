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

import os

import FreeCAD
import FreeCADGui

App = FreeCAD
Gui = FreeCADGui


# define the name of the directory to be created
TEST_WORKING_BASE_DIRECTORY = "/tmp/FreeCADtest/"


class AWorkingDirectoryTest(unittest.TestCase):

    @classmethod
    def setUpDirectory(cls, working_directory):
        cls._working_directory = working_directory
        cls._working_directory_full_path = TEST_WORKING_BASE_DIRECTORY + cls._working_directory
        try:
            if os.path.exists(cls._working_directory_full_path):
                for subDir in os.listdir(cls._working_directory_full_path):
                    os.remove(os.path.join(cls._working_directory_full_path, subDir))
                # os.rmdir(TEST_WORKING_BASE_DIRECTORY)
        except OSError:
            cls.fail(cls, "Cannot Clean up test directory: %s failed" % cls._working_directory_full_path)
        try:
            if not os.path.exists(cls._working_directory_full_path):
                os.makedirs(cls._working_directory_full_path)
        except OSError:
            cls.fail(cls, "Cannot create test directory: %s failed" % cls._working_directory_full_path)

    @classmethod
    def getDirectory(cls):
        return cls._working_directory

    @classmethod
    def getDirectoryFullPath(cls):
        return cls._working_directory_full_path

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        # Close all documents in FreeCAD
        document_list = list(App.listDocuments().keys())
        for document_name in document_list:
            App.closeDocument(document_name)
