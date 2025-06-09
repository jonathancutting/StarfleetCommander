class Planet:
    def __init__(self, detail:dict):
        # data members (instance variables)
        self.id = detail["id"]
        self.name = detail["name"]
        self.location = parseLocation(detail["location"])
        self.resources = {}
        self.mines = {}
        self.ships = {}
        self.defences = {}
        self.tasks = {}
        self.summary = {}

def parseLocation(loc:str) -> dict:
    '''
    Parses the combined location string into a dictionary containing the parts.

    Args:
        loc (str):  combined location string containing the full location. For
                    example, "15:450:5m".
    
    Returns:
        dict (str, str):    dictionary containing separated galaxy, system, and
                            planet slot locations.
    '''
    location = {}

    elems = loc.split(":")
    location["galaxy"] = elems[0]
    location["system"] = elems[1]
    location["slot"] = elems[2]

    return location
