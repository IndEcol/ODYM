class ODYMBaseClass:
    """
    Class with the object definition for a data object (system, process, flow, ...) in ODYM
    """
    def __init__(self, Name=None, ID=None, UUID=None):
        """ Basic initialisation of Obj."""
        self.Name            = Name # object name
        self.ID              = ID   # object ID
        self.UUID            = UUID # object UUID
        self.Aspects         = {'Time': 'Model time','Cohort': 'Age-cohort','OriginProcess':'Process where flow originates','DestinationProcess':'Destination process of flow','OriginRegion': 'Region where flow originates from','DestinationRegion': 'Region where flow is bound to', 'Good': 'Process, good, or commodity', 'Material': 'Material: ore, alloy, scrap type, ...','Element': 'Chemical element' } # Define the aspects of the system variables
        self.Dimensions      = {'Time': 'Time', 'Process':'Process', 'Region': 'Region', 'Good': 'Process, good, or commodity', 'Material': 'Material: ore, alloy, scrap type, ...','Element': 'Chemical element' } # Define the dimensions of the system variables
