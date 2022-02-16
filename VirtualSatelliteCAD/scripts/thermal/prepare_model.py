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

"""
    This script is used to assign the correct face numbers in the VirSat model definition.
    It imitates the geometric manipulations in the main script
    (during which additional faces are created and the old face numbers are no longer valid)
    so that one can obtain the face numbers after executing this script
    and use them in face-related properties in VirSat (e.g. face heat load, radiation properties)
"""

import FreeCAD
import BOPTools.SplitFeatures # NOQA
import Part # NOQA
import os

App = FreeCAD
Log = FreeCAD.Console.PrintLog
Err = FreeCAD.Console.PrintError


def make_contact_faces(path):
    """
    This function preprocesses the geometrical model:
    It creates new parts that have the same geometry as the original ones, but also the contact areas are seperate faces

    The folder at path has to contains the exported geometry and contact information
    """
    # Object list to add all parts to for generating the boolean fragment
    objectList = []

    def is_mesh_or_spreadsheet(obj):
        return obj.TypeId not in ['Fem::FemMeshObjectPython', 'Spreadsheet::Sheet'] and obj.Label != "BooleanFragments"

    # Iterate over all combinations of 2 objects in the active document
    for object1 in App.ActiveDocument.Objects:
        if is_mesh_or_spreadsheet(object1):
            objectList.append(object1)

            for object2 in App.ActiveDocument.Objects:
                if is_mesh_or_spreadsheet(object2):

                    success = overlap_objects(object1, object2, path)
                    if not success:
                        return False

    # Initialize the boolean fragment object
    booleanFragments = BOPTools.SplitFeatures.makeBooleanFragments(name='BooleanFragments')
    # Add all parts from the object list to the boolean fragment
    booleanFragments.Objects = objectList
    # Mode of boolean fragment generation is standard
    booleanFragments.Mode = 'Standard'
    # Execute the creation of the boolean fragment
    booleanFragments.Proxy.execute(booleanFragments)
    booleanFragments.ViewObject.Visibility = False

    # Iterate through all objects in the boolean fragment
    for obj in App.ActiveDocument.BooleanFragments.Objects:
        prev_label = obj.Label.replace("_temp", "").replace("001", "")
        obj.ViewObject.Visibility = False

        # Create the new object as common between the old object and the boolean fragment#
        newObject = App.ActiveDocument.BooleanFragments.Shape.common(obj.Shape)
        # Set the label of all objects in the boolean fragment to ....+"_old"
        obj.Label = prev_label+"_old"
        Part.show(newObject, prev_label)
        App.ActiveDocument.getObject(prev_label).ViewObject.Visibility = True

    return True


def overlap_objects(object1, object2, path):
    """
        Cuts object overlaps
    """

    Log("Trying to overlap objects: " + object1.Label + ", " + object2.Label + "\n")
    com = object1.Shape.common(object2.Shape)
    if object1.Label != object2.Label and com.Volume > 0:
        Log("Overlap between "+object1.Label+" and "+object2.Label+" detected.\n")

        masterFile = path + "validateContactsMaster.txt"
        slaveFile = path + "validateContactsSlave.txt"
        if not os.path.isfile(masterFile):
            Err(masterFile + " does not exists")
            return False
        if not os.path.isfile(slaveFile):
            Err(slaveFile + " does not exists")
            return False

        with open(masterFile) as masterContacts, open(slaveFile) as slaveContacts:
            masterObjects = masterContacts.readlines()
            slaveObjects = slaveContacts.readlines()
            for i, masterObject in enumerate(masterObjects):

                expectedMasterName = sanitizeName(masterObject)
                expectedSlaveName = sanitizeName(slaveObjects[i])
                if (expectedMasterName == object2.Label and expectedSlaveName == object1.Label):
                    prev_label = object1.Label
                    object1.Label = prev_label + "_vanilla"
                    Part.show(object1.Shape.cut(object2.Shape), prev_label)
                    Log("Slave "+object1.Label+" was cut successfully at the overlap.\n")
                else:
                    Log("Nothing was cut this time at: " + expectedMasterName + " " + expectedSlaveName + "\n")

    return True


def sanitizeName(obj):
    raw_name = obj.replace("\n", "").split(",")[0]
    object_name = raw_name.split("_")[0]
    object_uuid = "___".join(raw_name.split("_")[1:])
    return object_name + "_" + object_uuid


def desanitizeName(name):
    return name.replace("___", "_")


def reset():
    """
        Removes objects created by make_contact_faces
    """
    for obj in App.ActiveDocument.Objects:
        if obj.TypeId == 'Fem::FemMeshObjectPython' or obj.TypeId == 'Fem::FeaturePython' or obj.TypeId == 'Part::Feature' or obj.Label == "BooleanFragments":
            App.ActiveDocument.removeObject(obj.Name)
    for obj in App.ActiveDocument.Objects:
        old_label = obj.Label
        new_label = old_label.replace("_old", "").replace("001", "").replace("_vanilla", "")
        obj.Label = new_label
        obj.ViewObject.Visibility = True
