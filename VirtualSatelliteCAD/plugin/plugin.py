import abc
import typing


class Plugin(metaclass=abc.ABCMeta):
    '''
    Abstract definitions of a FreeCADMod plugin
    '''

    def __init__(self, name, directory, hasPreferencesUi):
        self.name = name
        self.directory = directory
        self.hasPreferencesUi = hasPreferencesUi

    @abc.abstractmethod
    def importToDict(self) -> typing.Dict[str, str]:
        '''
        Import information via a plugin specific interface.
        Has to return the internal data structure.
        Will be called by the CommandImport.
        '''
        return

    @abc.abstractmethod
    def exportFromDict(self, data_dict: typing.Dict[str, str]):
        '''
        Export information from the internal data structure
        via a plugin specific interface.
        Will be called by the CommandExport.
        '''
        return
