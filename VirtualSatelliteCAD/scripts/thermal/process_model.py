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
import Part # NOQA
import ObjectsFem # NOQA
import BOPTools.SplitFeatures # NOQA
from femmesh.gmshtools import GmshTools as gt # NOQA
from scripts.thermal.prepare_model import reset, make_contact_faces, sanitizeName, desanitizeName
import os

App = FreeCAD
Gui = FreeCADGui
Log = FreeCAD.Console.PrintLog
Err = FreeCAD.Console.PrintError


def process_model(path):
    """
    Processes the thermal information
    """
    checkFile(path + "main.inp")
    checkFile(path + "Sun_Vector.csv")
    checkFile(path + "Solar_Intensity.csv")
    checkFile(path + "Earth_Vector.csv")
    checkFile(path + "meshSizes.txt")
    checkFile(path + "validateContactsMaster.txt")
    checkFile(path + "validateContactsSlave.txt")

    reset()
    open(path + "Amp.inp", 'w')
    Log("Amp.inp cleared\n")

    with open(path + "main.inp") as mainFile:
        main = mainFile.readlines()
        includeOrbitRadiation = False

        if any("*INCLUDE, INPUT=Amp.inp" in line for line in list(main)):
            includeOrbitRadiation = True
            Log("Amp.inp to be generated\n")
        else:
            includeOrbitRadiation = False

    sunData = getSunData(path, "Sun_Vector.csv", "Solar_Intensity.csv")
    earthData = getEarthData(path, "Earth_Vector.csv")

    make_contact_faces(path)
    contactFaces = findAllContacts(path)
    hideAllFaces()

    createMeshAndGroupsAndInputFile(path, contactFaces, includeOrbitRadiation, sunData, earthData)

    writeContactToInput(path, contactFaces)
    applyVolumeFlux(path)


def checkFile(file):
        if not os.path.isfile(file):
            Err(file + " does not exists")
            return False


def findAllContacts(path):
    """
    This function finds all (area) contacts and writes the involved parts and faces into a list.
    Found contacts are validated using validateContactsMaster.txt and validateContactsSlave.txt
    """
    masterContactFaces = []
    slaveContactFaces = []
    masterContactMeshSize = []
    slaveContactMeshSize = []
    contactNumber = []

    # Iterate through all objects (-1 because object2 will be the missing last one)
    for i in range(0, len(App.ActiveDocument.Objects)-1):

        # Choose starting obj
        object1 = App.ActiveDocument.Objects[i]
        # Ensure that part type fits (avoid errors because of tabular objects)
        if object1.TypeId == 'Part::Feature' and "_old" not in object1.Label:
            # Iterate through all objects
            # i+1 because no need to choose same objects or objects that have been checked already
            for j in range(i+1, len(App.ActiveDocument.Objects)):

                object2 = App.ActiveDocument.Objects[j]
                if object2.TypeId == 'Part::Feature' and "_old" not in object1.Label:
                    # Iterate through all faces of object1
                    for k in range(0, len(object1.Shape.Faces)):

                        face1 = object1.Shape.Faces[k]
                        # Iterate through all faces of object2
                        for l in range(0, len(object2.Shape.Faces)):

                            face2 = object2.Shape.Faces[l]
                            # Initialize distance between elements
                            distance = 0.0
                            sec = face1.section(face2)

                            # Check for circular faces
                            # sec.Edges == 1 meaning the contact is defined by one edge only,
                            # limiting the contact to either edge, or round face (edge contacts to be dismissed)
                            if len(sec.Edges) == 1 and len(face1.Edges) == 1 and len(face2.Edges) == 1:
                                # Iterate through all vertexes (fixpoints that define a surface) of face2
                                for vertex in face2.Vertexes:
                                    # Check distance of every single vertex of face 2 to the unrestrained (infinite) surface of face1
                                    d = vertex.distToShape(face1.Surface.toShape())[0]
                                    distance += d
                                for vertex in face1.Vertexes:
                                    # Check distance of every single vertex of face 1 to the unrestrained (infinite) surface of face2
                                    d = vertex.distToShape(face2.Surface.toShape())[0]
                                    distance += d
                                # Check if tolerance is exceeded
                                if distance <= 0.01:
                                    Log("Contact detected between Face " + str(k+1) + " of " + object1.Label
                                        + " and Face " + str(l+1) + " of " + object2.Label + ".\n")
                                    # Validate if contact is actually defined in VirSat
                                    confirmation, index, meshSizeMaster, meshSizeSlave = validateContact(path, object1, object2)
                                    if confirmation is True:
                                        Log("A contact between the bodies is validated by the Virtual Satellite model!\n")
                                        # Add validated contact to contact list
                                        masterContactFaces.append([object1.Label, k+1])
                                        slaveContactFaces.append([object2.Label, l+1])
                                        masterContactMeshSize.append(meshSizeMaster)
                                        slaveContactMeshSize.append(meshSizeSlave)
                                        contactNumber.append(index+1)
                                    else:
                                        Log("A contact between the bodies is NOT defined in the Virtual Satellite model!\n")
                                else:
                                    Log("No Contact detected between Face " + str(k+1) + " of " + object1.Label +
                                        " and Face " + str(l+1) + " of " + object2.Label + ".\n")
                            # Check for (partly) angular faces
                            elif len(sec.Edges) > 1 and len(face1.Wires) == 1 and len(face2.Wires) == 1:
                                if len(face1.Vertexes) == len(face2.Vertexes):
                                    numberOfCommonVertexes = 0
                                    for vertex1 in face1.Vertexes:
                                        for vertex2 in face2.Vertexes:
                                            if(round(vertex1.Point[0], 3) == round(vertex2.Point[0], 3)
                                               and round(vertex1.Point[1], 3) == round(vertex2.Point[1], 3)
                                               and round(vertex1.Point[2], 3) == round(vertex2.Point[2], 3)):
                                                numberOfCommonVertexes += 1
                                    if len(face1.Vertexes) == numberOfCommonVertexes:
                                        Log("Contact detected between Face " + str(k+1) + " of " + object1.Label +
                                            " and Face " + str(l+1) + " of " + object2.Label + ".\n")
                                        # Validate if contact is actually defined in VirSat
                                        confirmation, index, meshSizeMaster, meshSizeSlave = validateContact(path, object1, object2)
                                        if confirmation is True:
                                            Log("A contact between the bodies is validated by the Virtual Satellite model!\n")
                                            # Add validated contact to contact list
                                            masterContactFaces.append([object1.Label, k+1])
                                            slaveContactFaces.append([object2.Label, l+1])
                                            masterContactMeshSize.append(meshSizeMaster)
                                            slaveContactMeshSize.append(meshSizeSlave)
                                            contactNumber.append(index+1)
                            else:
                                Log("No Contact detected between Face " + str(k+1) + " of " + object1.Label +
                                    " and Face " + str(l+1) + " of " + object2.Label + ".\n")
                else:
                    Log(object2.Label+" has not the right shape.\n")
        else:
            Log(object1.Label+" has not the right shape.\n")
    return (masterContactFaces, slaveContactFaces, contactNumber, (masterContactMeshSize, slaveContactMeshSize))

# ===========================
# FUNCTIONS FOR MESH CREATION
# ===========================


def createMeshAndGroupsAndInputFile(path, contactFaces, includeOrbitRadiation, sunData, earthData):
    """
    Function for creating mesh, mesh groups and the input file out of the first two
    """
    # TODO
    checkFile(path + "meshSizes.txt")

    # Saves the number of nodes that are already defined to keep node set consistent throughout all elements
    nrOfGivenNodes = 0
    # Saves the number of elements that are already defined to keep element set consist throughout all elements
    nrOfGivenElements = 0
    currentNumberOfMeshFaces = 0
    # List to store all small mesh faces that belong to a certain body face
    facesOnContactFace = []
    predefinedMeshList = []

    with open(path + "meshSizes.txt", 'r') as meshSizesInput:
        content = meshSizesInput.readlines()
        meshSizes = []
        objectNames = []

        for i in range(0, len(content)):
            meshSizes.append(content[i].replace("\n", "").split(",")[1])
            objectNames.append(sanitizeName(content[i].replace("\n", "").split(",")[0]))

    for obj in App.ActiveDocument.Objects:
        Log(obj.TypeId)
        if obj.TypeId == 'Fem::FemMeshObjectPython':
            predefinedMeshList.append(obj.Label.replace("001", ""))
            femmesh_object = ObjectsFem.makeMeshGmsh(App.ActiveDocument, obj.Label.replace("001", "") + "_Mesh")
            femmesh_object.Part = obj.Part
            femmesh_object.FemMesh = obj.FemMesh
            App.ActiveDocument.removeObject(obj.Name)
    Log("Meshlist")
    Log(predefinedMeshList)

    for obj in App.ActiveDocument.Objects:
        # Make sure chosen obj is not a mesh or spreadsheet obj
        if (obj.TypeId == 'Part::Feature' and obj.TypeId != 'Fem::FemMeshObjectPython'
                and "_old" not in obj.Label and "_vanilla" not in obj.Label):
            if obj.Label not in predefinedMeshList:
                Log("Not in Meshlist")
                Log(obj.Label)
                # Set characteristic mesh length [mm]
                characteristicMeshLengthMax = meshSizes[objectNames.index(obj.Label)]
                femmesh_object = ObjectsFem.makeMeshGmsh(App.ActiveDocument, obj.Label+"_Mesh")
                femmesh_object.Part = obj
                femmesh_object.CharacteristicLengthMax = characteristicMeshLengthMax
                gmsh_mesh = gt(femmesh_object)

                # Mesh region creation starts here
                # Iterate through all contacts
                for i in range(0, len(contactFaces[0])):
                    if contactFaces[0][i][0] == obj.Label:
                        regionCharLength = contactFaces[3][0][i]
                        region = ObjectsFem.makeMeshRegion(
                            FreeCAD.ActiveDocument, femmesh_object, regionCharLength,
                            "Region_MasterContact_" + contactFaces[0][i][0].partition('_')[0] + "_To_" + contactFaces[1][i][0].partition('_')[0])
                        region.References = (obj, "Face"+str(contactFaces[0][i][1]))

                    if contactFaces[1][i][0] == obj.Label:
                        regionCharLength = contactFaces[3][1][i]
                        region = ObjectsFem.makeMeshRegion(
                            FreeCAD.ActiveDocument, femmesh_object, regionCharLength,
                            "Region_SlaveContact_" + contactFaces[0][i][0].partition('_')[0] + "_To_" + contactFaces[1][i][0].partition('_')[0])
                        region.References = (obj, "Face"+str(contactFaces[1][i][1]))

                gmsh_mesh.create_mesh()
                # change setting that all groups are also created as node groups (probably not necessary?)
                femmesh_object.GroupsOfNodes = True

            elif obj.Label in predefinedMeshList:
                Log("Object " + obj.Label + " has a predefined mesh that is used.\n")
                femmesh_object = App.ActiveDocument.getObject(obj.Label+"_Mesh")
                femmesh_object.Part = obj

            # Export mesh to input file
            exportobj = App.ActiveDocument.getObject(obj.Label+"_Mesh")
            exportobj.FemMesh.writeABAQUS(path+desanitizeName(obj.Label)+".inp", 1, True)

            # Calculation of orientation of mesh faces and assignment of solar radiation loads
            if includeOrbitRadiation is True:
                currentNumberOfMeshFaces = writeAmplitudeFile(obj, femmesh_object, path, currentNumberOfMeshFaces, nrOfGivenElements, sunData, earthData)

            # Mesh postprocessing starts here
            # Change node and element numbers to make the sets consistent
            makeInputConsecutive(
                nrOfGivenNodes, femmesh_object.FemMesh.NodeCount, nrOfGivenElements,
                femmesh_object.FemMesh.VolumeCount, path + desanitizeName(obj.Label) + ".inp")
            # Add a node set for every single component to assign volume flux to
            addNodesetForObject(path, obj, nrOfGivenNodes, femmesh_object.FemMesh.NodeCount)
            # Add an element set for every single component to assign material to
            addElementsetForObject(path, obj, nrOfGivenElements, femmesh_object.FemMesh.VolumeCount)

            # Difference between original element number and new element number
            Log("Volumes " + str(femmesh_object.FemMesh.Volumes))
            elementNumberDifference = nrOfGivenElements - femmesh_object.FemMesh.Volumes[0] + 1

            Log("For " + obj.Label + " the difference between generated element number and " +
                "reassigned element number is: "+str(elementNumberDifference) + "\n")

            for i in range(0, len(contactFaces[0])):
                if contactFaces[0][i][0] == obj.Label:
                    with open(path + desanitizeName(obj.Label) + ".inp", 'a') as geoFile:
                        facesOnContactFace = femmesh_object.FemMesh.getccxVolumesByFace(
                            femmesh_object.Part.Shape.Faces[contactFaces[0][i][1]-1])
                        geoFile.write("\n*SURFACE, NAME=" + "Master_Contact_" + contactFaces[0][i][0].partition('_')[0]
                                      + "_TO_" + contactFaces[1][i][0].partition('_')[0]+"\n")
                        for j in range(0, len(facesOnContactFace)):
                            geoFile.write(str(facesOnContactFace[j][0]+elementNumberDifference) +
                                          ", S" + str(facesOnContactFace[j][1]) + "\n")

                if contactFaces[1][i][0] == obj.Label:
                    with open(path + desanitizeName(obj.Label) + ".inp", 'a') as geoFile:
                        facesOnContactFace = femmesh_object.FemMesh.getccxVolumesByFace(
                            femmesh_object.Part.Shape.Faces[contactFaces[1][i][1]-1])
                        geoFile.write("\n*SURFACE, NAME="+"Slave_Contact_"+contactFaces[1][i][0].partition('_')[0]
                                      + "_TO_" + contactFaces[0][i][0].partition('_')[0] + "\n")
                        for j in range(0, len(facesOnContactFace)):
                            geoFile.write(str(facesOnContactFace[j][0]+elementNumberDifference) +
                                          ", S" + str(facesOnContactFace[j][1]) + "\n")

            setFaceEmissivities(path, femmesh_object, elementNumberDifference)
            applyHeatFluxBoundaryConditions(path, femmesh_object, elementNumberDifference)
            applyTemperatureBoundaryConditions(path, femmesh_object, nrOfGivenNodes)

            # adjust element and node number parameters for next iteration
            nrOfGivenNodes += femmesh_object.FemMesh.NodeCount
            nrOfGivenElements += femmesh_object.FemMesh.VolumeCount
            Log("Total assigned Nodes: "+str(nrOfGivenNodes)+"\n")

        else:
            Log(obj.Label + " is of type" + obj.TypeId + " and not Part::Feature\n")
    Log("Mesh and Mesh Group generation completed.\n")
    Log(str(currentNumberOfMeshFaces)+"\n")


def hideAllFaces():
    """
    Hide all faces of regular or python parts
    """
    for obj in Gui.ActiveDocument.Document.Objects:
        if obj.TypeId == 'Part::FeaturePython':
            obj.ViewObject.Visibility = False
        if obj.TypeId == 'Part::Feature':
            guiObject = Gui.ActiveDocument.getObject(obj.Label)
            try:
                colorTuple = list(guiObject.DiffuseColor)
                for i in range(0, len(colorTuple)):
                    colorTupleInTuple = list(colorTuple[i])
                    colorTupleInTuple[3] = 1.0
                    colorTuple[i] = tuple(colorTupleInTuple)
                guiObject.ViewObject.DiffuseColor = tuple(colorTuple)
            except Exception:
                Log("Object " + obj.Label + " has no GUI representation."+"\n")


def showAllFaces():
    """
    Show all faces of regular or python parts
    """
    for obj in Gui.ActiveDocument.Document.Objects:
        if obj.TypeId == 'Part::FeaturePython':
            obj.Visibility = True
        if obj.TypeId == 'Part::Feature':
            guiObject = Gui.ActiveDocument.getObject(obj.Label)
            try:
                colorTuple = list(guiObject.DiffuseColor)
                for i in range(0, len(colorTuple)):
                    colorTupleInTuple = list(colorTuple[i])
                    colorTupleInTuple[3] = 0.0
                    colorTuple[i] = tuple(colorTupleInTuple)
                obj.ViewObject.DiffuseColor = tuple(colorTuple)
            except Exception:
                Log("Object " + obj.Label + " has no GUI representation."+"\n")

# =======================
# FUNCTIONS FOR CONTACTS
# ======================


def validateContact(path, object1, object2):
    """
    Cross check if detected contacts are also defined in Virtual Satellite
    """
    # Read the two files created by VirSat with the component names in it
    with open(path+"validateContactsMaster.txt", 'r') as readerMaster, open(path + "validateContactsSlave.txt", 'r') as readerSlave:
        masterObjects = readerMaster.readlines()
        slaveObjects = readerSlave.readlines()
        # Initialize return value as false
        validation = False

        comb1 = object1.Label+object2.Label
        comb2 = object2.Label+object1.Label
        # Iterate through the number of components in the files from VirSat
        for i in range(0, len(masterObjects)):
            # For every component pair in the file: check if the same combination exists in FreeCAD
            if (comb1 == sanitizeName(masterObjects[i]) + sanitizeName(slaveObjects[i])
                    or comb2 == sanitizeName(masterObjects[i]) + sanitizeName(slaveObjects[i])):
                # If so set validation parameter to true
                validation = True

            if validation is True:
                meshSizeMaster = masterObjects[i].replace("\n", "").split(",")[1]
                meshSizeSlave = slaveObjects[i].replace("\n", "").split(",")[1]
                return (True, i, meshSizeMaster, meshSizeSlave)

        return(False, 0, 0, 0)


def writeContactToInput(path, contactFaces):
    """
    Write the detected and validated contacts to the input file
    """
    # Create input file for contact definition
    with open(path + "contact_surfaces.inp", 'w') as add_contact:
        # For all validated contacts write them to input
        for i in range(0, len(contactFaces[0])):
            add_contact.write("\n\n*CONTACT PAIR,INTERACTION=SI" + str(contactFaces[2][i]) + ",TYPE=SURFACE TO SURFACE\n")
            add_contact.write(
                "Master_Contact_" + contactFaces[0][i][0].partition('_')[0] + "_TO_" +
                contactFaces[1][i][0].partition('_')[0] + "," + "Slave_Contact_" +
                contactFaces[1][i][0].partition('_')[0] + "_TO_" + contactFaces[0][i][0].partition('_')[0] + "\n")
        return ("add_contact.inp ready!")


# ===========================
# FUNCTIONS FOR PREPROCESSING
# ===========================

def getSunData(path, filenameVec, filenameInt):
    sunData = []
    with open(path+filenameVec, 'r') as vectorData:
        vectorList = vectorData.readlines()
        with open(path+filenameInt, 'r') as intensityData:
            intensities = intensityData.readlines()
            for i in range(1, len(vectorList)-1):
                vector = (
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[1],
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[2],
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[3])
                intensity = str(intensities[i]).replace('\n', '').replace('\\n', '').split(",")[1]
                sunData.append((vector, intensity))
    Log(str(sunData)+"\n")
    return sunData


def getEarthData(path, filenameVec):
    earthData = []
    with open(path+filenameVec, 'r') as vectorData:
        vectorList = vectorData.readlines()
        for i in range(1, len(vectorList)-1):
            vector = (
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[1],
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[2],
                    str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[3])
            reflectionAngle = str(vectorList[i]).replace('\n', '').replace('\\n', '').split(",")[4]
            earthData.append((vector, reflectionAngle))
    Log(str(earthData)+"\n")
    return earthData


# ============================
# FUNCTIONS FOR POSTPROCESSING
# ============================


def writeAmplitudeFile(obj, femmesh_object, path, currentNumberOfMeshFaces, nrOfGivenElements, sunData, earthData):
    # Sets the sector (liens) in the input file where elements are defined
    elementDefinitionArea = (femmesh_object.FemMesh.NodeCount + 5 + 5, femmesh_object.FemMesh.NodeCount + 5 + 4 + femmesh_object.FemMesh.VolumeCount)

    checkFile(path + desanitizeName(obj.Label) + ".inp")
    checkFile(path + desanitizeName(obj.Label) + ".rd")
    with open(path + desanitizeName(obj.Label) + ".inp", 'r') as meshFile:
        with open(path + desanitizeName(obj.Label) + ".rd", 'r') as radFile:
            with open(path + "Amp.inp", 'a') as ampFile:
                content = meshFile.readlines()
                radProperties = radFile.readlines()
                n = 1
                # Iterate through all faces of the obj and get the according fem mesh elements and their faces
                for face in obj.Shape.Faces:
                    faceIrAbsorptivity = 1-float(radProperties[0].replace('\n', '').replace('\\n', '').split(",")[1])
                    faceAbsorptivity = float(radProperties[0].replace('\n', '').replace('\\n', '').split(",")[2])
                    for i in range(1, len(radProperties)):
                        if int(radProperties[i].split(",")[0]) == n:
                            faceIrAbsorptivity = 1-float(radProperties[n].replace('\n', '').replace('\\n', '').split(",")[1])
                            faceAbsorptivity = float(radProperties[n].replace('\n', '').replace('\\n', '').split(",")[2])
                    # Get the fem elements and their faces for the obj face
                    ccxVolumes = femmesh_object.FemMesh.getccxVolumesByFace(face)

                    # Iterate through all fem element faces that are part of the obj face
                    for i in range(0, len(ccxVolumes)):
                        # Get the element number and the element face number (1,2,3 or 4 for tetrahedrons)
                        elementNumber, elementFaceNumber = ccxVolumes[i][0], ccxVolumes[i][1]
                        line = str(content[elementDefinitionArea[0]+elementNumber-femmesh_object.FemMesh.Volumes[0]-1]
                                   ).replace('\n', '').replace('\\n', '').split(",")

                        if elementFaceNumber == 1:
                            # For an explanation which nodes comprise which face see CalculiX manual (e.g. under *RADIATE)
                            # The nodes which are part of the mesh element and form the corresponding face are extracted from the input file
                            # Depending on the face number within the element (1..4) different nodes represent the face
                            nodeNumber1 = int(line[1])
                            nodeNumber2 = int(line[2])
                            nodeNumber3 = int(line[3])

                        elif elementFaceNumber == 2:
                            nodeNumber1 = int(line[1])
                            nodeNumber2 = int(line[4])
                            nodeNumber3 = int(line[2])

                        elif elementFaceNumber == 3:
                            nodeNumber1 = int(line[2])
                            nodeNumber2 = int(line[4])
                            nodeNumber3 = int(line[3])

                        elif elementFaceNumber == 4:
                            nodeNumber1 = int(line[3])
                            nodeNumber2 = int(line[4])
                            nodeNumber3 = int(line[1])

                        node1 = femmesh_object.FemMesh.getNodeById(nodeNumber1)
                        node2 = femmesh_object.FemMesh.getNodeById(nodeNumber2)
                        node3 = femmesh_object.FemMesh.getNodeById(nodeNumber3)

                        norm = findMeshFaceNormal(node1, node2, node3)

                        # Used for information AND Amplitude Numbers in Amp file. Do not change position/order
                        currentNumberOfMeshFaces += 1

                        ampFile.write("\n**FaceNormal:" + str(norm[0]) + "," + str(norm[1]) + "," + str(norm[2]))
                        ampFile.write("\n*AMPLITUDE,NAME=A" + str(currentNumberOfMeshFaces) + "\n")
                        for k in range(0, len(sunData)):
                            # The cosine of the sun angle to the face normal is used to calculate the total intensity
                            cosineSunAngleToFaceNormal = getCosineOfAngleBetweenVectors(norm, sunData[k][0])
                            cosineEarthAngleToFaceNormal = getCosineOfAngleBetweenVectors(norm, earthData[k][0])
                            cosineEarthSunAngle = float(earthData[k][1])
                            if cosineSunAngleToFaceNormal < 0 or determineObstruction(node1, sunData[k][0]) is True:
                                resultingSunIntensityOnFace = 0
                            else:
                                # Cosine of sun angle and visibility of sun due to earth obstruction (0 or 100) are combined for the total sun intensity(factor)
                                resultingSunIntensityOnFace = round(1367*faceAbsorptivity*cosineSunAngleToFaceNormal*float(sunData[k][1])/100, 2)
                            if cosineEarthAngleToFaceNormal < 0 or determineObstruction(node1, earthData[k][0]) is True:
                                resultingIrEarthIntensityOnFace = 0
                                resultingAlbedoIntensityOnFace = 0
                            else:
                                resultingIrEarthIntensityOnFace = round(250*faceIrAbsorptivity*cosineEarthAngleToFaceNormal, 2)
                                if float(sunData[k][1]) > 0:
                                    resultingAlbedoIntensityOnFace = round(0.35 * 1367 * faceAbsorptivity * cosineEarthAngleToFaceNormal * cosineEarthSunAngle *
                                                                           float(sunData[k][1])/100, 2)
                                else:
                                    resultingAlbedoIntensityOnFace = 0
                            ampFile.write(str((k+1)) + ", " + str(round(resultingSunIntensityOnFace + resultingIrEarthIntensityOnFace +
                                                                        resultingAlbedoIntensityOnFace, 2)) + "\n")
                        ampFile.write("\n*DFLUX, AMPLITUDE=A"+str(currentNumberOfMeshFaces)+"\n")
                        ampFile.write(str(elementNumber+nrOfGivenElements-femmesh_object.FemMesh.Volumes[0]+1)+",S"+str(elementFaceNumber)+",1\n")
        Log("Amp.inp created successfully!")
        return currentNumberOfMeshFaces


def makeInputConsecutive(nodesGiven, nodeCount, elementsGiven, elementCount, filepath):
    """
    Function for adjusting all node numbers such that they are consecutive and no duplicated numbers are assigned
    Changes the node and element numbers of the single meshes such that they are consecutive and not assigned multiple times
    """

    pathnew = filepath

    # Sets the sector (lines) in the input file where nodes are defined
    nodeDefinitionArea = (5, nodeCount + 4 + 1)
    # Sets the sector (liens) in the input file where elements are defined
    elementDefinitionArea = (nodeCount + 5 + 4, nodeCount + 5 + 4 + elementCount)
    # Number of nodes in the current mesh
    n = nodeCount
    # Number of elements in the current mesh
    e = elementCount

    with open(filepath, 'r') as inputFile:
        text = inputFile.readlines()
        with open(pathnew, 'w') as output:
            # Cycle through file lines (backwards, for elements to be handled first.
            # "for" loop in node area takes advantage of the already interpreted line)
            for ln in range(len(text)-1, 0, -1):
                # After the element definition area, node groups are created -> all values + nodesGiven
                # (remember element groups are added AFTER this function is called -> no risk of mistaking elements and nodes)
                if ln > elementDefinitionArea[1]:
                    if text[ln].isnumeric():
                        text[ln] = int(text[ln]) + nodesGiven
                # If counter within element definition sector: get line, remove characters and split into list
                if elementDefinitionArea[0] <= ln < elementDefinitionArea[1]:
                    text[ln] = str(text[ln]).replace('\n', '').replace('\\n', '').split(",")
                    text[ln][0] = elementsGiven + e
                    for col in range(1, len(text[ln])):
                        text[ln][col] = str(int(text[ln][col]) + nodesGiven)
                    e -= 1
                # If counter within node definition sector: get line, remove characters and split into list
                if nodeDefinitionArea[0] <= ln < nodeDefinitionArea[1]:
                    text[ln] = str(text[ln]).replace('\n', '').replace('\\n', '').split(",")
                    text[ln][0] = nodesGiven + n
                    n -= 1
            text[2] = "**"+str(nodeCount)+","+str(elementCount)
            for ln in range(0, len(text)):
                outputLine = str(text[ln]).replace("[", "").replace("]", "").replace("'", "")
                output.write(outputLine+"\n")


def addNodesetForObject(path, obj, nrOfGivenNodes, nrOfNodes):
    """
    For the given object with the number of already existing nodes and the number of nodes in the object, add a nodeset with all nodes of the obj
    """
    with open(path + desanitizeName(obj.Label) + ".inp", 'a') as output:
        output.write("\n*NSET,NSET="+obj.Label.partition("_")[0]+", GENERATE\n")
        output.write(str(nrOfGivenNodes+1)+","+str(nrOfGivenNodes+nrOfNodes)+"\n")


def addElementsetForObject(path, obj, nrOfGivenElements, nrOfElements):
    """
    For the given object with the number of already existing elements and the number of elements in the object,
    add a element set with all elements of the object
    """
    with open(path + desanitizeName(obj.Label) + ".inp", 'a') as output:
        output.write("\n*ELSET,ELSET="+obj.Label.partition("_")[0]+", GENERATE\n")
        output.write(str(nrOfGivenElements+1)+","+str(nrOfGivenElements+nrOfElements)+"\n")


def applyVolumeFlux(path):
    for obj in App.ActiveDocument.Objects:
        if obj.TypeId == 'Fem::FemMeshObjectPython':
            name = path+desanitizeName(obj.Label.replace("_Mesh", "")) + ".bfl"
            checkFile(name)
            with open(name, 'r') as file:
                content = file.readlines()
                if len(content[0].split(",")) < 2:
                    volFluxTotal = float(content[0])
                    with open(path+obj.Label.replace("_Mesh", "") + ".bfl", 'w') as output:
                        output.write(obj.Label.partition("_")[0]+",BF,"+str(volFluxTotal*1000000/obj.FemMesh.Volume).replace("1/mm^3", ""))
                else:
                    Log(obj.Label+" volume heat flux already defined!")


def applyHeatFluxBoundaryConditions(path, femobject, elementNumberDifference):

    name = path+desanitizeName(femobject.Part.Label)+".ehf"
    checkFile(name)
    with open(name, 'r') as bcFileIn:
        content = bcFileIn.readlines()
        name = path+desanitizeName(femobject.Part.Label)+".ehf"
        checkFile(name)
        with open(name, 'w') as bcFileOut:
            if len(content) > 0:
                for i in range(0, len(content)):
                    faceNumber = int(str(content[i]).replace('\n', '').replace('\\n', '').split(",")[0])
                    flux = str(content[i]).replace('\n', '').replace('\\n', '').split(",")[1]
                    face = femobject.Part.Shape.Faces[faceNumber-1]
                    ccxVolumes = femobject.FemMesh.getccxVolumesByFace(face)
                    for i in range(0, len(ccxVolumes)):
                        bcFileOut.write(str(ccxVolumes[i][0]+elementNumberDifference)+', S'+str(ccxVolumes[i][1])+', '+flux+"\n")


def applyTemperatureBoundaryConditions(path, femobject, nrOfGivenNodes):
    name = path+desanitizeName(femobject.Part.Label)+".bcf"
    checkFile(name)
    with open(name, 'r') as bcFileIn:
        content = bcFileIn.readlines()
        name = path+desanitizeName(femobject.Part.Label)+".bc"
        checkFile(name)
        with open(name, 'w') as bcFileOut:
            if len(content) > 0:
                for i in range(0, len(content)):
                    lineLength = len(str(content[i]).replace('\n', '').replace('\\n', '').split(","))
                    if lineLength > 1:
                        faceNumber = int(str(content[i]).replace('\n', '').replace('\\n', '').split(",")[0])
                        temp = str(content[i]).replace('\n', '').replace('\\n', '').split(",")[1]
                        face = femobject.Part.Shape.Faces[faceNumber-1]
                        nodes = femobject.FemMesh.getNodesByFace(face)
                        bcFileOut.write("\n*BOUNDARY\n")
                        for i in range(0, len(nodes)):
                            bcFileOut.write(str(nodes[i]+nrOfGivenNodes)+',11,11, '+temp+"\n")
                    if lineLength == 1:
                        temp = str(content[0]).replace('\n', '').replace('\\n', '').split(",")[0]
                        bcFileOut.write("\n*BOUNDARY\n")
                        bcFileOut.write(str(femobject.Part.Label.partition('_')[0]+",11,11,"+temp+"\n"))


def setFaceEmissivities(path, femmesh_object, elementNumberDifference):
    """
    Should be executed AFTER makeContactFaces() and meshing!
    """
    name = path+desanitizeName(femmesh_object.Part.Label)+".rd"
    checkFile(name)
    with open(name, 'r') as readRad:
        radInfo = readRad.readlines()
        radFaces = []
        radValues = []
        temp = 3.0
        name = path + femmesh_object.Part.Label + ".rad"
        checkFile(name)
        with open(name, 'w') as writeRad:
            # For all face infos contained in rad file, write face number and emissivity to lists
            for i in range(1, len(radInfo)):
                radFaces.append(int(str(radInfo[i]).replace('\n', '').replace('\\n', '').split(",")[0]))
                radValues.append(float(str(radInfo[i]).replace('\n', '').replace('\\n', '').split(",")[1]))
            for i in range(0, len(femmesh_object.Part.Shape.Faces)):
                face = femmesh_object.Part.Shape.Faces[i]
                # Obtain fem element numbers and element faces for active part face
                ccxVolumes = femmesh_object.FemMesh.getccxVolumesByFace(face)
                # If value for emissivity of the specific face was provided by VirSat set this value
                if i+1 in radFaces:
                    emissivity = radValues[radFaces.index(i+1)]
                    for j in range(0, len(ccxVolumes)):
                        writeRad.write(str(ccxVolumes[j][0]+elementNumberDifference) + ', R' +
                                       str(ccxVolumes[j][1]) + 'CR, ' + str(temp) + ', ' + str(emissivity) + "\n")
                # Else set emissivity to general component value
                else:
                    emissivity = str(radInfo[0]).replace('\n', '').replace('\\n', '').split(",")[1]
                    for j in range(0, len(ccxVolumes)):
                        writeRad.write(str(ccxVolumes[j][0] + elementNumberDifference) + ', R' +
                                       str(ccxVolumes[j][1]) + 'CR, ' + str(temp) + ', ' + str(emissivity) + "\n")
            Log("Radiation file for "+femmesh_object.Part.Label+" created successfully!")


# ==================================================================
# HELPER FUNCTIONS (probably could be replaced with numpy functions)
# ==================================================================


def findMeshFaceNormal(nodeCoord1, nodeCoord2, nodeCoord3):
    """
    Function to find the normal of a plane defined by three nodes
    """
    # Calculate two vectors from pairs of nodes
    vec1 = [nodeCoord1[0]-nodeCoord2[0], nodeCoord1[1]-nodeCoord2[1], nodeCoord1[2]-nodeCoord2[2]]
    vec2 = [nodeCoord1[0]-nodeCoord3[0], nodeCoord1[1]-nodeCoord3[1], nodeCoord1[2]-nodeCoord3[2]]
    # Calculate the normal by calculating the cross product of the two vectors
    norm = crossProduct(vec1, vec2)
    return norm


def crossProduct(vec1, vec2):
    """
    Function to calculate the cross product of two vectors
    """
    crossProduct = [vec1[1]*vec2[2]-vec1[2]*vec2[1], vec1[2]*vec2[0]-vec1[0]*vec2[2], vec1[0]*vec2[1]-vec1[1]*vec2[0]]
    return crossProduct


def getCosineOfAngleBetweenVectors(vector1, vector2):
    """
    Calculate the cosine of the angle between two vectors and return the value
    """
    dotProduct = float(vector1[0])*float(vector2[0])+float(vector1[1])*float(vector2[1])+float(vector1[2])*float(vector2[2])
    amountVec1 = (float(vector1[0])**2+float(vector1[1])**2+float(vector1[2])**2)**(1/2)
    amountVec2 = (float(vector2[0])**2+float(vector2[1])**2+float(vector2[2])**2)**(1/2)
    cosineOfAngle = dotProduct/(amountVec1*amountVec2)
    return (cosineOfAngle)


def determineObstruction(node1, node2):
    edge = Part.makeLine(node1, node2)
    for obj in App.ActiveDocument.Objects:
        if obj.TypeId not in ['Fem::FemMeshObjectPython', 'Spreadsheet::Sheet', 'Fem::FeaturePython', 'Part::Feature'] and obj.Label != "BooleanFragments":
            intersec = edge.common(obj.Shape)
            if len(intersec.Vertexes) > 0:
                return True
    return False
