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

TEST_JSON_PART_BOX = """{
        "color": 12632256,
        "shape": "BOX",
        "name": "Beam",
        "lengthX": 0.04,
        "lengthY": 0.02,
        "lengthZ": 0.01,
        "radius": 0.0,
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
    }"""

TEST_JSON_PART_CONE = """{
        "name": "Beam",
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
        "shape": "CONE",
        "lengthX": 0.0,
        "lengthY": 0.5,
        "lengthZ": 0.0,
        "radius": 0.2,
        "color": 12632256
    }"""

TEST_JSON_PART_CYLINDER = """{
        "color": 12632256,
        "shape": "CYLINDER",
        "name": "Tube",
        "lengthX": 0.0,
        "lengthY": 0.1,
        "lengthZ": 0.0,
        "radius": 0.05,
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
    }"""

TEST_JSON_PART_SPHERE = """{
        "color": 12632256,
        "shape": "SPHERE",
        "name": "Tube",
        "lengthX": 0.0,
        "lengthY": 0.0,
        "lengthZ": 0.0,
        "radius": 0.003,
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022"
    }"""

TEST_JSON_PART_GEOMETRY = """{
        "color": 66280,
        "shape": "GEOMETRY",
        "name": "Geometry",
        "lengthY": 1.0,
        "lengthX": 0.0,
        "radius": 1.0,
        "lengthZ": 0.0,
        "uuid": "38eae3a5-8338-4a51-b1df-5583058f9e77",
        "stlPath": "Test.stl"
    }"""

TEST_JSON_PART_NONE = """{
        "name": "Beam",
        "uuid": "6201a731-d703-43f8-ab37-6a0581dfe022",
        "shape": "NONE",
        "lengthX": 0.04,
        "lengthY": 0.01,
        "lengthZ": 0.3,
        "radius": 0.0,
        "color": 12632256,
        "stlPath" : "testfile.stl"
    }"""

TEST_JSON_PRODUCT_WITH_CHILDREN = """{
        "name": "BasePlateBottom1",
        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
        "partName": "BasePlate",
        "posX": 1.0,
        "posY": 2.0,
        "posZ": 3.0,
        "rotX": 0.349,
        "rotY": 0.698,
        "rotZ": 1.046,
        "children": [
            {
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 0.0,
                "rotX": 0.0,
                "children": [
                ],
                "rotZ": 0.0,
                "rotY": 0.0,
                "name": "BasePlateBottom2",
                "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
                "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate"
            },
            {
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 0.5,
                "rotX": 0.0,
                "children": [
                ],
                "rotZ": 0.0,
                "rotY": 0.0,
                "name": "BasePlateTop",
                "uuid": "a199e3bd-3bc1-426d-8321-e9bd829339b3",
                "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate"
            }
        ]
    }
    """

TEST_JSON_PRODUCT_WITH_CHILD_WITH_CHILD = """{
        "name": "BasePlateBottom1",
        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
        "partName": "BasePlate",
        "posX": 10.0,
        "posY": 15.0,
        "posZ": 20.0,
        "rotX": 0.349,
        "rotY": 0.698,
        "rotZ": 1.046,
        "children": [
            {
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 0.0,
                "rotX": 0.0,
                "children": [
                {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.5,
                    "rotX": 0.0,
                    "children": [
                    ],
                    "rotZ": 0.0,
                    "rotY": 0.0,
                    "name": "BasePlateTop",
                    "uuid": "a199e3bd-3bc1-426d-8321-e9bd829339b3",
                    "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                    "partName": "BasePlate"
                }
                ],
                "rotZ": 0.0,
                "rotY": 0.0,
                "name": "BasePlateBottom2",
                "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
                "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate"
            }
        ]
    }
    """

TEST_JSON_PRODUCT_WITHOUT_CHILDREN = """{
        "name": "BasePlateBottom",
        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
        "partName": "BasePlate",
        "posX": 0.02,
        "posY": 0.03,
        "posZ": 0.04,
        "rotX": 0.3490659,
        "rotY": 0.6981317,
        "rotZ": 1.0471976,
        "children": [
        ]
    }
    """

TEST_JSON_PRODUCT_WITH_ONE_CHILD = """{
        "name": "BasePlateBottom",
        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
        "partName": "BasePlate",
        "posX": 0.02,
        "posY": 0.03,
        "posZ": 0.04,
        "rotX": 0.3490659,
        "rotY": 0.6981317,
        "rotZ": 1.0471976,
        "children": [
            {
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 0.0,
                "rotX": 0.0,
                "children": [
                ],
                "rotZ": 0.0,
                "rotY": 0.0,
                "name": "BasePlateBottom",
                "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484",
                "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                "partName": "BasePlate"
            }
        ]
    }
    """
