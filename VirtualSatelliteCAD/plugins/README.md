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

@Plugin.register
class MyPlugin(Plugin):
    def importToDict(self, project_directory):
        return
    def exportFromDict(self, data_dict, project_directory):
        return
register_plugin(MyPlugin(display_name, directory_name, providesUi))
```
The newly created ```MyPlugin``` extends the base class ```Plugin``` and registers itself via ```register_plugin```.

## Providing preferences
The preferences page can be extended by providing a *preferences.ui* and setting ```providesUi``` to ```True``` in the ```MyPlugin``` class's constructor.

The UI extension is a full ui file created by Qt Designer (see https://wiki.freecadweb.org/Workbench_creation/en).
With layout it could look like this:

```XML
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>894</width>
    <height>621</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>NAME</string>
  </property>
  <layout class="QVBoxLayout">
   <property name="spacing">
    <number>6</number>
   </property>
   <property name="leftMargin">
    <number>9</number>
   </property>
   <property name="topMargin">
    <number>9</number>
   </property>
   <property name="rightMargin">
    <number>9</number>
   </property>
   <property name="bottomMargin">
    <number>9</number>
   </property>
   <item>
    <widget class="QGroupBox" name="groupBox">
     <property name="title">
      <string>TITLE</string>
     </property>
     <layout class="QVBoxLayout" name="verticalLayout">
      <!--> Insert further items here <-->
      <item>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <spacer name="verticalSpacer">
     <property name="orientation">
      <enum>Qt::Vertical</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>20</width>
       <height>40</height>
      </size>
     </property>
    </spacer>
   </item>
  </layout>
 </widget>
 <customwidgets>
  <customwidget>
   <!--> References to custom FreeCAD widgets <-->
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>

```