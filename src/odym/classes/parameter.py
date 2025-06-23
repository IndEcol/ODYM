from odym.classes.base import ODYMBaseClass


class Parameter(ODYMBaseClass):
    """
    Class with the definition and methods for parameters
    """

    def __init__(self, Name = None, ID = None, UUID = None, P_Res = None, MetaData = None, Indices = None, Values=None, Uncert=None, Unit = None):
        """ Basic initialisation of a parameter."""
        super().__init__(Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.P_Res       = P_Res   # id of process to which parameter is assigned (id: int)
        self.Indices     = Indices # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'
        self.MetaData    = MetaData # Dictionary with additional metadata

        self.Values      = Values   # parameter values, np.array, multidimensional, unit is Unit
        self.Uncert      = Uncert  # uncertainty of value in %
        self.Unit        = Unit   # Unit of parameter values