import os
import FreeCAD
from plugin.plugin import Plugin

PLUGIN_DIR_NAME = "plugins"
Log = FreeCAD.Console.PrintLog
Err = FreeCAD.Console.PrintError
plugins = []


def loadPlugins(module_path):
    '''
    Crawls all directories in the plugin directory.
    For each directory: if an init file exists, it is executed.

    We expect that the provided plugin registers itself by calling registerPlugin().
    This mechanism works similar to the FreeCAD extension mechanism,
    used e.g. by this FreeCADMod.
    '''
    Log("Importing Virtual Satellite Plugins\n")
    plugin_dir = os.path.join(module_path, PLUGIN_DIR_NAME)

    Log(os.listdir(plugin_dir))
    for dir_name in os.listdir(plugin_dir):
        dir_path = os.path.join(plugin_dir, dir_name)
        plugin_path = os.path.join(dir_path, "init_plugin.py")
        if os.path.isdir(dir_path) or os.path.exists(plugin_path):
            try:
                with open(file=plugin_path, encoding="utf-8") as f:
                    exec(f.read())
            except Exception:
                Log('Init:      Initializing ' + dir_path + '... failed\n')
            else:
                Log('Init:      Initializing ' + dir_path + '... done\n')


def registerPlugin(plugin):
    '''
    Registers a new concrete Plugin
    '''
    if isinstance(plugin, Plugin):
        Err('Registered plugin:' + plugin.name + '\n')
        plugins.append(plugin)
    else:
        Err(plugin.name + 'is not a plugin\n')
