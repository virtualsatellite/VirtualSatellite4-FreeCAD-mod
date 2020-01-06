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

TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD = """{
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
                    {
                        "posX": 0.5,
                        "posY": 0.5,
                        "posZ": 0.5,
                        "rotX": 0.0,
                        "children": [
                        ],
                        "rotZ": 0.0,
                        "rotY": 0.0,
                        "name": "BasePlateBottom3",
                        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45485",
                        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                        "partName": "BasePlate"
                    }
                ],
                "rotZ": 0.3490659,
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

TEST_JSON_PRODUCT_WITH_CHILDREN_WITH_CHILD_SUBASSEMBLY_IS_NO_PART = """{
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
                    {
                        "posX": 0.5,
                        "posY": 0.5,
                        "posZ": 0.5,
                        "rotX": 0.0,
                        "children": [
                        ],
                        "rotZ": 0.0,
                        "rotY": 0.0,
                        "name": "BasePlateBottom3",
                        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45485",
                        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                        "partName": "BasePlate"
                    }
                ],
                "rotZ": 0.3490659,
                "rotY": 0.0,
                "name": "BasePlateBottom2",
                "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45484"
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

TEST_JSON_PRODUCT_SUBASSEMBLY_WITH_SAME_PART = """{
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
                    {
                        "posX": 0.5,
                        "posY": 0.5,
                        "posZ": 0.5,
                        "rotX": 0.0,
                        "children": [
                        ],
                        "rotZ": 0.0,
                        "rotY": 0.0,
                        "name": "BasePlateBottom3",
                        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45485",
                        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                        "partName": "BasePlate"
                    }
                ],
                "rotZ": 0.3490659,
                "rotY": 0.0,
                "name": "BasePlate",
                "uuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
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

TEST_JSON_PRODUCT_ROOT = """{
        "name": "Root",
        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45480",
        "children": [
            {
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
                        "name": "BasePlateBottom2",
                        "uuid": "e8794f3d-86ec-44c5-9618-8b7170c45485",
                        "partUuid": "3d3708fd-5c6c-4af9-b710-d68778466084",
                        "partName": "BasePlate"
                    }
                ]
            }
        ]
    }
    """

TEST_JSON_FULL_NONE_SHAPE = """{
    "Products": {
        "name": "NoneShape",
        "uuid": "a3533e02-125c-4066-bffe-d046d8d8342a",
        "children": [{
                "name": "None",
                "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 1.0,
                "rotX": 0.0,
                "rotY": 0.0,
                "rotZ": 0.0,
                "partUuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                "partName": "None",
                "children": []
            }
        ]
    },
    "Parts": [{
            "name": "None",
            "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
            "shape": "NONE",
            "lengthX": 1.0,
            "lengthY": 1.0,
            "lengthZ": 0.02,
            "radius": 0.05,
            "color": 32768
        }]
}"""

TEST_JSON_FULL_NONE_SHAPE_ASSEMBLY = """{
    "Products": {
        "name": "NoneShapeAssembly",
        "uuid": "a3533e02-125c-4066-bffe-d046d8d8342a",
        "children": [{
            "posX": 0.0,
            "posY": 0.0,
            "posZ": 0.5,
            "rotX": 0.0,
            "children": [{
                "name": "None",
                "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                "posX": 0.0,
                "posY": 0.0,
                "posZ": 1.0,
                "rotX": 0.0,
                "rotY": 0.0,
                "rotZ": 0.0,
                "partUuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                "partName": "None",
                "children": []
            }
            ],
            "rotZ": 0.0,
            "rotY": 0.0,
            "name": "NoneAssembly",
            "uuid": "2afb23c9-f458-4bdb-a4e7-fc863364644f",
            "partUuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
            "partName": "None"
        }]
    },
    "Parts": [{
            "name": "None",
            "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
            "shape": "NONE",
            "lengthX": 1.0,
            "lengthY": 1.0,
            "lengthZ": 0.02,
            "radius": 0.05,
            "color": 32768
        }]
}"""

TEST_JSON_FULL_VISCUBE = """{
        "Products": {
            "children": [{
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 1.0,
                    "rotX": 0.0,
                    "children": [],
                    "rotZ": 0.0,
                    "rotY": 0.0,
                    "name": "Top",
                    "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                    "partUuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                    "partName": "Top"
                }, {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "children": [],
                    "rotZ": 0.0,
                    "rotY": 0.0,
                    "name": "Bottom",
                    "uuid": "61db0622-6fef-4f12-932d-a00fdb9d0848",
                    "partUuid": "00f430a6-6311-4a33-961b-41ded4cf57d5",
                    "partName": "Plate"
                }, {
                    "posX": 0.5,
                    "posY": 0.0,
                    "posZ": 0.5,
                    "rotX": 0.0,
                    "children": [],
                    "rotZ": 0.0,
                    "rotY": 1.5707963267948966,
                    "name": "Front",
                    "uuid": "e6af9d3f-8ad6-4488-b3d0-d35549be9a1e",
                    "partUuid": "e6af9d3f-8ad6-4488-b3d0-d35549be9a1e",
                    "partName": "Front"
                }, {
                    "posX": -0.5,
                    "posY": 0.0,
                    "posZ": 0.5,
                    "rotX": 0.0,
                    "children": [],
                    "rotZ": 0.0,
                    "rotY": 1.5707963267948966,
                    "name": "Back",
                    "uuid": "a3c9c547-8fd3-40d5-97a1-a3f9a3a9c337",
                    "partUuid": "a3c9c547-8fd3-40d5-97a1-a3f9a3a9c337",
                    "partName": "Back"
                }, {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.5,
                    "rotX": 0.0,
                    "children": [{
                            "posX": 0.0,
                            "posY": 0.5,
                            "posZ": 0.0,
                            "rotX": 1.5707963267948966,
                            "children": [],
                            "rotZ": 0.0,
                            "rotY": 0.0,
                            "name": "Left",
                            "uuid": "615985c0-73fd-48db-8f8b-e11b7cbb2ee8",
                            "partUuid": "615985c0-73fd-48db-8f8b-e11b7cbb2ee8",
                            "partName": "Left"
                        }, {
                            "posX": 0.0,
                            "posY": -0.5,
                            "posZ": 0.0,
                            "rotX": 1.5707963267948966,
                            "children": [],
                            "rotZ": 0.0,
                            "rotY": 0.0,
                            "name": "Right",
                            "uuid": "882a0b35-7da8-4555-903d-fd6b5cbec392",
                            "partUuid": "882a0b35-7da8-4555-903d-fd6b5cbec392",
                            "partName": "Right"
                        }
                    ],
                    "rotZ": 0.0,
                    "rotY": 0.0,
                    "name": "BeamStructure",
                    "uuid": "2afb23c9-f458-4bdb-a4e7-fc863364644f",
                    "partUuid": "2afb23c9-f458-4bdb-a4e7-fc863364644f",
                    "partName": "BeamStructure"
                }
            ],
            "name": "SpaceCube",
            "uuid": "a3533e02-125c-4066-bffe-d046d8d8342a"
        },
        "Parts": [{
                "color": 16744448,
                "shape": "CYLINDER",
                "name": "BeamStructure",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "2afb23c9-f458-4bdb-a4e7-fc863364644f",
                "lengthZ": 1.0
            }, {
                "color": 8388608,
                "shape": "BOX",
                "name": "Right",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "882a0b35-7da8-4555-903d-fd6b5cbec392",
                "lengthZ": 0.02
            }, {
                "color": 32832,
                "shape": "BOX",
                "name": "Front",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "e6af9d3f-8ad6-4488-b3d0-d35549be9a1e",
                "lengthZ": 0.02
            }, {
                "color": 16711680,
                "shape": "BOX",
                "name": "Left",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "615985c0-73fd-48db-8f8b-e11b7cbb2ee8",
                "lengthZ": 0.02
            }, {
                "color": 65280,
                "shape": "BOX",
                "name": "Plate",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "00f430a6-6311-4a33-961b-41ded4cf57d5",
                "lengthZ": 0.02
            }, {
                "color": 16776960,
                "shape": "BOX",
                "name": "Back",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "a3c9c547-8fd3-40d5-97a1-a3f9a3a9c337",
                "lengthZ": 0.02
            }, {
                "color": 32768,
                "shape": "BOX",
                "name": "Top",
                "lengthY": 1.0,
                "lengthX": 1.0,
                "radius": 0.05,
                "uuid": "cc14e2c7-9d7e-4cf2-8d6d-9b8cf5e96d56",
                "lengthZ": 0.02
            }
        ]
    }
    """
