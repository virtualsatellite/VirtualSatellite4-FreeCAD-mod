class Plugin:
    '''
    Abstract definitions of a FreeCADMod plugin
    '''

    def __init__(self, name, directory, hasPreferencesUi):
        self.name = name
        self.directory = directory
        self.hasPreferencesUi = hasPreferencesUi
