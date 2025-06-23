import numpy as np

from odym.classes.base import ODYMBaseClass


class Stock(ODYMBaseClass):  # Flow needs to at least have dimension time x element
    """
    Class with the definition and methods for a stock in ODYM
    """

    def __init__(
        self,
        Name=None,
        ID=None,
        UUID=None,
        P_Res: int = None,
        Indices: str = None,
        Type: int = None,
        Values: np.ndarray = None,
        Uncert=None,
        Unit: str = None,
        Color: str = None,
    ):
        """Basic initialisation of a stock."""
        super().__init__(
            Name=Name, ID=ID, UUID=UUID
        )  # Hand over parameters to parent class init
        self.P_Res = P_Res  # id of process where stock resides (id: int)
        self.Indices = Indices  # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'
        self.Type = Type  # Type is an int value, indicating: 0: stock, 1: (net) stock change or addition to stock, 2: removal from stock

        self.Values = (
            Values  # flow values, np.array, multidimensional, unit is system-wide unit
        )
        self.Uncert = Uncert  # uncertainty of value in %
        self.Unit = Unit  # Unit string

        self.Color = Color  # color as string 'R,G,B', where each of R, G, B has a value of 0...255
