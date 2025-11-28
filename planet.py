class Planet:
    def __init__(self):
        # data members (instance variables)
        self.id = ""
        self.name = ""
        self.location = {}
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
    location = {"galaxy":0, "system":0, "slot":0, "moon":False}
    try:
        elems = loc.split(":")
        location["galaxy"] = int(elems[0])
        location["system"] = int(elems[1])
        if str(elems[2])[-1] == "m":
            location["slot"] = int(elems[2][:-1])
            location["moon"] = True
        else:
            location["slot"] = int(elems[2])
            location["moon"] = False
    except (ValueError, TypeError) as e:
        print(f"Problem loading planet location.")

    return location
