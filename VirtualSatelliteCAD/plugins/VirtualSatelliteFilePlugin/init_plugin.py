import FreeCAD
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin

Log = FreeCAD.Console.PrintMessage


@Plugin.register
class VirSatFilePlugin(Plugin):
    '''
    Legacy Plugin that directly im-/exports a JSON file
    '''
    def importToDict(self, project_directory):
        from PySide2.QtWidgets import QFileDialog
        import json

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getOpenFileName(
            None,  # ui parent
            "Open JSON file",  # dialog caption
            project_directory,
            "JSON(*.json)")[0]

        if filename != '':
            (f"Selected file '{filename}'\n")

            with open(filename, 'r') as f:
                try:
                    return json.load(f)
                except ValueError as error:
                    Log(f"ERROR: Invalid JSON found: '{error}'\n")
                    Log("Please provide a valid JSON\n")
        return

    def exportFromDict(self, data_dict, project_directory):
        from PySide2.QtWidgets import QFileDialog
        import json

        # call pyqt dialog: returns (filename, filter)
        filename = QFileDialog.getSaveFileName(
            None,  # ui parent
            "Save JSON file",  # dialog caption
            project_directory,
            "JSON(*.json)")[0]
        if filename != '':
            json_str = json.dumps(data_dict)

            with open(filename, 'w') as file:
                file.write(json_str)


register_plugin(VirSatFilePlugin("Virtual Satellite File Plugin (Legacy)", "VirtualSatelliteFilePlugin", False))
