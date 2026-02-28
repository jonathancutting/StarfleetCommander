import logging      # built-in Python logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)    # set module-level logger object

@dataclass
class Location:
    galaxy: int
    system: int
    slot: int
    moon: bool

@dataclass
class Resources:
    ore: int
    crystal: int
    hydrogen: int

@dataclass
class Mines:
    ore: int
    crystal: int
    hydrogen: int

@dataclass
class Fleet:
    shadow: int = 0
    genesis: int = 0
    hermes: int = 0
    helios: int = 0
    artemis: int = 0
    atlas: int = 0
    apollo: int = 0
    zagreus: int = 0
    charon: int = 0
    hercules: int = 0
    dionysus: int = 0
    poseidon: int = 0
    carmanor: int = 0
    gaia: int = 0
    athena: int = 0
    ares: int = 0
    hades: int = 0
    prometheus: int = 0
    zeus: int = 0
    hephaestus: int = 0

@dataclass
class Defences:
    missile: int = 0
    laser: int = 0
    pulse: int = 0
    particle: int = 0
    abm: int = 0
    decoy: int = 0
    ibm: int = 0
    gauss: int = 0
    large_decoy: int = 0
    plasma: int = 0

class Planet:
    def __init__(self):
        # data members (instance variables)
        self.id = ""
        self.name = ""
        self.location = Location(0, 0, 0, False)
        self.resources = Resources(0, 0, 0)
        self.mines = Mines(0, 0, 0)
        self.ships = Fleet()
        self.defences = Defences()
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