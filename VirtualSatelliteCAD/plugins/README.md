# FreeCADMod plugin mechanism

## Plugin structure
To create a new plugin simply create or import a new directory having the following file structure:

```
.
+-- init_plugin.py
+-- preferences.ui (optional)
```

The code in *init_plugin.py* will be executed on plugin discovery and is the entry point to your plugin. 

## Minimal plugin
A minimal plugin looks like this:
```python
from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin

class MyPlugin(Plugin):
    pass

register_plugin(MyPlugin(display_name, directory_name, providesUi))
```
The newly created ```MyPlugin``` extends the base class ```Plugin``` and registers itself via ```register_plugin```.

## Providing preferences
The preferences page can be extended by providing a *preferences.ui* and setting ```providesUi``` to ```True``` in the ```MyPlugin``` class's constructor.

The UI extension is a widget created by Qt Designer (see https://wiki.freecadweb.org/Workbench_creation/en):
```XML
<widget class="QGroupBox" name="name">
</widget>
```