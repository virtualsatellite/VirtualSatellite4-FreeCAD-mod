import FreeCAD
from plugin.plugin_loader import registerPlugin
from plugin.plugin import Plugin

Log = FreeCAD.Console.PrintLog
Log("Called init of plugin\n")


class ConcretePlugin(Plugin):
    pass


registerPlugin(ConcretePlugin("name"))
