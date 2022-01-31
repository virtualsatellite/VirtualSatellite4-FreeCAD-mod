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
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin


@Plugin.register
class VirSatPlugin(Plugin):
    '''
    Plugin that connects to a Virtual Satellite Server
    '''
    def __init__(self, name, directory, hasPreferencesUi):
        super().__init__(name, directory, hasPreferencesUi)

        import FreeCAD
        self.preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/VirtualSatelliteREST")

    def importToDict(self, project_directory):
        from plugins.VirtualSatelliteRestPlugin.importer import VirSatRestImporter
        from PySide2.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QDialogButtonBox
        import FreeCAD
        Msg = FreeCAD.Console.PrintMessage
        Err = FreeCAD.Console.PrintError

        Msg('Starting import via Virtual Satellite REST API\n')

        api_instances, repo_name, setup_successful = self.getPreferences()
        if not setup_successful:
            Err('Setup was not successful, aborting import\n')
            return

        # Get a starting SEI from the preferences
        start_sei_uuid = None
        if(self.preferences.GetBool('AskForStartingSEI')):
            # Get all available SEIs
            from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
            root_seis, seis = TreeCrawler().crawl_raw_seis(api_instances, repo_name)

            # Get display names
            class SelectSeiDialog(QDialog):
                def __init__(self, root_seis, seis):
                    PS_CONCEPT = 'de.dlr.sc.virsat.model.extension.ps'

                    super(SelectSeiDialog, self).__init__()
                    self.selectedSei = None

                    self.setWindowTitle("Select starting SEI")
                    self.setMinimumWidth(500)
                    self. buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

                    self.tree = QTreeWidget()

                    self.tree.setHeaderLabels(["Name", "Uuid"])

                    def fillTreeRecursive(item, sei):
                        for child_ref in sei['children']:
                            child_sei = seis[child_ref['uuid']]
                            _type = child_sei['type']
                            # Only applicable for selected elements types:
                            if(_type == PS_CONCEPT + '.ElementConfiguration' or _type == PS_CONCEPT + '.ElementOccurence'):
                                childItem = QTreeWidgetItem(item, [child_sei['name'], child_sei['uuid']])
                                fillTreeRecursive(childItem, child_sei)

                    for uuid, root_sei in root_seis.items():
                        _type = root_sei['type']
                        # Only applicable for selected trees:
                        if(_type == PS_CONCEPT + '.ConfigurationTree' or _type == PS_CONCEPT + '.AssemblyTree'):
                            item = QTreeWidgetItem(self.tree, [root_sei['name'], uuid])
                            fillTreeRecursive(item, root_sei)

                    self.vlayout = QVBoxLayout()

                    self.vlayout.addWidget(self.tree)

                    self.vlayout.addWidget(self.buttons)

                    self.buttons.accepted.connect(self.acceptSelection)
                    self.buttons.rejected.connect(self.reject)
                    self.setLayout(self.vlayout)

                def acceptSelection(self):
                    self.selectedSei = self.tree.currentItem().text(1)
                    self.accept()

                @classmethod
                def show(cls, root_seis, seis):
                    dialog = cls(root_seis, seis)
                    dialog.exec_()
                    return dialog.selectedSei

            start_sei_uuid = SelectSeiDialog.show(root_seis, seis)
        elif(self.preferences.GetBool('UseStaticStartingSEI')):
            start_sei_uuid = self.preferences.GetString('StartingSEI')

        if start_sei_uuid is None:
            Err('No starting SEI defined\n')
            return None
        else:
            return VirSatRestImporter(project_directory, api_instances, repo_name).importToDict(start_sei_uuid)

    def exportFromDict(self, data_dict, project_directory):
        from plugins.VirtualSatelliteRestPlugin.exporter import VirSatRestExporter
        import FreeCAD
        Msg = FreeCAD.Console.PrintMessage
        Err = FreeCAD.Console.PrintError

        Msg('Starting export via Virtual Satellite REST API\n')

        api_instances, repo_name, setup_successful = self.getPreferences()
        if not setup_successful:
            Err('Setup was not successful, aborting export\n')
            return

        VirSatRestExporter().exportFromDict(data_dict, api_instances, repo_name)
        return

    def getPreferences(self):
        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch

        username = self.preferences.GetString('Username')
        password = self.preferences.GetString('Password')
        repo_name = self.preferences.GetString('RepositoryName')
        api_version_idx = self.preferences.GetInt('ApiVersion')

        adress = self.preferences.GetString('Hostadress')
        port = self.preferences.GetString('Port')
        if(self.preferences.GetBool('Http')):
            protocol = "http"
        else:
            protocol = "https"
        host = protocol + "://" + adress + ":" + port

        api_instances = ApiSwitch().get_apis(api_version_idx, host, username, password)

        can_connect = self.canConnectToServer((adress, port))
        setup_successful = api_instances is not None and can_connect

        import FreeCAD
        Err = FreeCAD.Console.PrintError
        if not can_connect:
            Err("Could not establish a server connection\n")

        return (api_instances, repo_name, setup_successful)

    def canConnectToServer(self, host):
        import socket
        try:
            socket.create_connection(host)
            return True
        except OSError:
            pass
        return False


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
