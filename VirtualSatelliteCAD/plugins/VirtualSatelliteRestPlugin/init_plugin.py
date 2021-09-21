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
    # TODO: test
    def __init__(self, name, directory, hasPreferencesUi):
        super().__init__(name, directory, hasPreferencesUi)

        import FreeCAD
        self.preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/VirtualSatelliteREST")

    def importToDict(self, project_directory):
        from plugins.VirtualSatelliteRestPlugin.importer import VirSatRestImporter

        from PySide2.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QDialogButtonBox

        api_instance, repo_name = self.getPreferences()
        # TODO: Get a starting SEI from the preferences
        # TODO: change to uuid??? or give whole sei if selected via dialog?
        start_sei_name = None  # 'ConfigurationTree'
        if(self.preferences.GetBool('AskForStartingSEI')):
            # Get all available SEIs
            from plugins.VirtualSatelliteRestPlugin.tree_crawler import TreeCrawler
            root_seis, seis, _, _ = TreeCrawler().crawlTree(api_instance, repo_name)

            # Get display names
            class SelectSeiDialog(QDialog):
                def __init__(self, root_seis, seis):
                    super(SelectSeiDialog, self).__init__()

                    self.setWindowTitle("New Group")
                    self.setGeometry(400, 400, 200, 200)

                    self.lab_a = QLabel('group name:')
                    self.lab_b = QLabel('Competition Events:')

                    self. buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

                    self.tree = QTreeWidget()

                    self.tree.setHeaderLabels(["Name", "Uuid"])

                    # TODO: check selection? some will result in errors???
                    def fillTreeRecursive(item, sei):
                        for child_ref in sei.children:
                            child_sei = seis[child_ref.uuid]
                            childItem = QTreeWidgetItem(item, [child_sei.name, child_sei.uuid])
                            fillTreeRecursive(childItem, child_sei)

                    for uuid, root_sei in root_seis.items():
                        item = QTreeWidgetItem(self.tree, [root_sei.name, uuid])
                        fillTreeRecursive(item, root_sei)

                    self.vlayout = QVBoxLayout()

                    self.vlayout.addWidget(self.tree)

                    self.vlayout.addWidget(self.buttons)

                    self.buttons.accepted.connect(self.accept)
                    self.buttons.rejected.connect(self.reject)
                    self.setLayout(self.vlayout)

                @classmethod
                def show(cls, root_seis, seis):
                    dialog = cls(root_seis, seis)
                    dialog.exec_()
                    # TODO: uuid?
                    return dialog.tree.currentItem().text(0)

            start_sei_name = SelectSeiDialog.show(root_seis, seis)
        elif(self.preferences.GetBool('UseStaticStartingSEI')):
            start_sei_name = self.preferences.GetString('StartingSEI')

        # TODO: nullcheck

        return VirSatRestImporter().importToDict(api_instance, repo_name, start_sei_name)

    def exportFromDict(self, data_dict, project_directory):
        from plugins.VirtualSatelliteRestPlugin.exporter import VirSatRestExporter

        # TODO: remove
        print(data_dict)
        api_instance, repo_name = self.getPreferences()

        VirSatRestExporter().exportFromDict(data_dict, api_instance, repo_name)
        return

    def getPreferences(self):
        from plugins.VirtualSatelliteRestPlugin.api_switch import ApiSwitch

        # TODO: remove comments
        username = self.preferences.GetString('Username')  # admin
        password = self.preferences.GetString('Password')  # secure
        repo_name = self.preferences.GetString('RepositoryName')  # visDemo
        api_version_idx = self.preferences.GetInt('ApiVersion')  # 0

        api_instance = ApiSwitch().get_api(api_version_idx, username, password)
        # TODO: nullcheck

        return (api_instance, repo_name)


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
