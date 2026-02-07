import logging      # built-in Python logging

logger = logging.getLogger(__name__)    # set module-level logger object

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
    Parses a location string like "15:450:5m" into a dict with galaxy, system,
    slot, and moon.

    :param loc: Location string in format "G:S:P" or "G:S:Pm" (m = moon)
    :type loc:  str
    :return:    dict with keys "galaxy", "system", "slot", and "moon"
    :rtype:     dict (str, int|bool)
    '''

    logger.debug("Planet location passed: %s", loc)
    location = {"galaxy":0, "system":0, "slot":0, "moon":False}

    try:
        elems = loc.strip().split(":")  # This will return a list of strings.
        if len(elems) != 3:             # Check that the list has exectly 3 elements.
            raise ValueError(f"Invalid location format \"{loc}\". Expected \"G:S:P\" or \"G:S:Pm\"")

        location["galaxy"] = int(elems[0])
        location["system"] = int(elems[1])

        if elems[2].endswith("m"):      # Detect if the location designates a moon.
            location["slot"] = int(elems[2][:-1])
            location["moon"] = True
        else:
            location["slot"] = int(elems[2])
            location["moon"] = False
        
        # Log successful parse.
        locStr = f"{location['galaxy']}:{location['system']}:{location['slot']}"
        if location["moon"]: locStr += "m"
        logger.debug("Parsed planet location: %s", locStr)

        return location

    except (ValueError, TypeError) as e:
        logger.exception("Could not parse planet location %s", loc)
        raise