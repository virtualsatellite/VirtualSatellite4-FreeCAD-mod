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
        ''' TODO
        Will be called by the CommandImport
        '''
        return

    @abc.abstractmethod
    def exportFromDict(self, data_dict: typing.Dict[str, str]):
        ''' TODO
        Will be called by the CommandExport
        '''
        return
