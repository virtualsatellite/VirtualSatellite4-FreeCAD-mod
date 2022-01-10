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
from module.environment import Environment, ICON_ABOUT
from PySide2.QtWidgets import QVBoxLayout, QLabel, QDialogButtonBox, QDialog


class CommandAbout:

    def Activated(self):
        dialog = QDialog()
        dialog.setWindowTitle('About Virtual Satellite FreeCADmod')

        verticalLayout = QVBoxLayout(dialog)

        label = QLabel()
        label.setText("""
            <html><head/><body>
            (c) Copyright by DLR (German Aerospace Center) Simulation and Software Technology 2020.<br>
            The DLR logo and DLR images are under copyright of DLR (German Aerospace Center),
            <a href=\"https://www.dlr.de/\">https://www.dlr.de/</a>.<br>
            The DLR logo and images cannot be altered or used without DLRs permission.<br>
            DLR logo and images are provided for the use under the following conditions
            <a href=\"https://www.dlr.de/EN/Service/Imprint/imprint_node.html\">https://www.dlr.de/EN/Service/Imprint/imprint_node.html</a>.
            </body></html>
        """)
        label.setOpenExternalLinks(True)

        buttonBox = QDialogButtonBox()
        buttonBox.setEnabled(True)
        buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(dialog.accept)

        verticalLayout.addWidget(label)
        verticalLayout.addWidget(buttonBox)

        dialog.exec_()

    def IsActive(self):
        return True

    def GetResources(self):
        return {'Pixmap': Environment().get_icon_path(ICON_ABOUT),
                'MenuText': 'About Virtual Satellite FreeCADmod',
                'ToolTip': 'Open the about dialog.'}
