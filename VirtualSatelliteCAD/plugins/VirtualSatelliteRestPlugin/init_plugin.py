from plugin.plugin_loader import register_plugin
from plugin.plugin import Plugin


@Plugin.register
class VirSatPlugin(Plugin):
    '''
    Plugin that connects to a Virtual Satellite Server
    '''
    def importToDict(self):
        return

    def exportFromDict(self, data_dict):
        return


register_plugin(VirSatPlugin("Virtual Satellite REST Plugin", "VirtualSatelliteRestPlugin", True))
