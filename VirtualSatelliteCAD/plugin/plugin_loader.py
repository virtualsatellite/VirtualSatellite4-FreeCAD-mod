import os
import FreeCAD
import traceback
from module.environment import Environment
from plugin.plugin import Plugin

Log = FreeCAD.Console.PrintLog
Err = FreeCAD.Console.PrintError
plugins = []


def load_plugins(module_path):
    '''
    Crawls all directories in the plugin directory.
    For each directory: if an init file exists, it is executed.

    We expect that the provided plugin registers itself by calling registerPlugin().
    This mechanism works similar to the FreeCAD extension mechanism,
    used e.g. by this FreeCADMod.
    '''
    Log("Importing Virtual Satellite Plugins\n")

    for dir_name in os.listdir(Environment().get_plugins_path()):
        dir_path = Environment().get_plugin_path(dir_name)
        plugin_path = os.path.join(dir_path, "init_plugin.py")
        if os.path.exists(plugin_path):
            try:
                with open(file=plugin_path, encoding="utf-8") as f:
                    exec(f.read())
            except Exception:
                Log('Init:      Initializing ' + dir_path + '... failed\n')
                Log(traceback.format_exc())
            else:
                Log('Init:      Initializing ' + dir_path + '... done\n')


def register_plugin(plugin):
    '''
    Registers a new concrete Plugin
    '''
    if isinstance(plugin, Plugin):
        Log('Registered plugin:' + plugin.name + '\n')
        plugins.append(plugin)
    else:
        Log(plugin.name + 'is not a plugin\n')
