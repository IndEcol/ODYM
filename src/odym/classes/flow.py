from odym.classes.base import ODYMBaseClass


class Flow(ODYMBaseClass):  # Flow needs to at least have dimension time x element
    """
    Class with the definition and methods for a flow in ODYM
    """

    def __init__(
        self,
        Name=None,
        ID=None,
        UUID=None,
        P_Start: int = None,
        P_End: int = None,
        Indices: str = None,
        Values=None,
        Uncert=None,
        Unit: str = None,
        Color: str = None,
    ):
        """Basic initialisation of a flow."""
        super().__init__(
            Name=Name, ID=ID, UUID=UUID
        )  # Hand over parameters to parent class init
        self.P_Start = P_Start  # id of start process of flow (id: int)
        self.P_End = P_End  # id of end process of flow (id: int)
        self.Indices = Indices  # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'

        self.Values = (
            Values  # flow values, np.array, multidimensional, unit is system-wide unit
        )
        self.Uncert = Uncert  # uncertainty of value in %
        self.Unit = Unit  # Unit string

        self.Color = Color  # color as string 'R,G,B', where each of R, G, B has a value of 0...255
