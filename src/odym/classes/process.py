from odym.classes.base import ODYMBaseClass
from odym.classes.parameter import Parameter
from odym.classes.flow import Flow


class Process(ODYMBaseClass):

    """
    Class with the definition and methods for a process in ODYM
    """

    def __init__(self, Name = None, ID = None, UUID = None, Bipartite = None, Graphical = None, Extensions = None, Parameters = None):
        """ Basic initialisation of a process."""
        super().__init__(Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.Bipartite = Bipartite   # For bipartite system graphs, a string with value 't' or 'd' for transformation and distribution process indicates which group the process belongs to.
        self.Extensions= Extensions  # Dictionary of
        self.Graphical = Graphical   # # Dictionary of graphical properties: xPos = None, yPos = None, Orientation = None, Color=None, Width = None, Height=None,

    def add_extension(self,Time = None, Name = None, Value=None, Unit = None, Uncert=None): # Extensions flows that are not part of the system-wide mass balance!
        if self.Extensions is None:
            self.Extensions = []
        self.Extensions.append(Flow(P_Start = self.ID, P_End = None, Time = Time, Name = Name, Unit = Unit, Value = Value, Uncert = Uncert))

    def add_parameter(self,Name = None):
        if self.Parameters is None:
            self.Parameters = []
        self.Parameters.append(Parameter(Value = None))
