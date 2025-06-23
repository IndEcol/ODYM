from odym.classes.base import ODYMBaseClass


class Classification(ODYMBaseClass):
    """
    Class for aspect classification
    """

    def __init__(self, Name = None, ID = None, UUID = None, Dimension = None, Items = None, IDs = None, AdditionalProporties = {}):
        """ Basic initialisation of an item list for alloys, materials, etc."""
        super().__init__(Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.Dimension         = Dimension # Dimension of classification: Time, Region, process, material, goods, ...
        self.Items             = Items # list with names of items
        self.IDs               = IDs # list with IDs of items
        self.AdditionalProps   = AdditionalProporties # Like population for regions, element composition for alloys, ...
