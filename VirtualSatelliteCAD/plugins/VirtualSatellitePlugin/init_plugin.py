import FreeCAD
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin

Log = FreeCAD.Console.PrintLog
Log("Called init of plugin\n")


class VirSatPlugin(Plugin):
    pass


register_plugin(VirSatPlugin("Virtual Satellite Plugin", "VirtualSatellitePlugin", True))
