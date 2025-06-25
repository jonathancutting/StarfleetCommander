import requests
import getpass
import shutil
import textwrap
from sfc import sendPostRequest

def login(cmd:dict[str, list[str]], s:requests.Session):
    '''
    Handles the "login" command from sfc main function.

    Args:
        cmd (dict):             Dictionary of the user-entered command string,
                                as parsed by the buildCommandDict function in
                                sfc.py. The dictionary should contain two 
                                elements: first, a string with the command, and
                                secondly, a list of strings with the arguments.
        s (requests.Session):   The user's request session object.
    
    Returns:
        None:   No returned objects.
    '''
    opts = parseArgs(cmd["args"])
    uname = ""
    pw = ""

    if len(opts) == 0: # no options and no arguments
        uname = getUsername()
        pw = getPassword()
    else:
        match opts[0]["opt"]:
            case "-h":
                optHelp()
                return
            case "-u":
                if len(opts[0]["args"]) > 0:
                    uname = opts[0]["args"][0]
                else:
                    uname = getUsername()
                pw = getPassword()
            case "-x":
                return
            case _:
                print(f"Unknown option '{opts[0]['opt']}'. Aborting login.")
                return
    
    print(f"Username: {uname}, Password: {pw}")
    body = buildRequestBody(uname, pw)
    url = "https://playstarfleet.com/login/authenticate"

    return

def parseArgs(pOpts:list[str]) -> list:
    '''
    Parses the arguments from the command dictionary and translates into a list
    of options appropriate for the login command.

    Args:
        pOpts (list[str]):  List containing the strings from the "args" element
                            in the command dictionary.

    Returns:
        list:   Returns a list of options elements. Each element is a dictionary
                with the form {"opt": str, "args": list[str]}.
    '''
    opts = []

    if len(pOpts) == 0: return opts

    if pOpts[0][0] != "-":
        print(f"Malformed option '{pOpts[0]}'. See login --help. Aborting login.")
        opts.append({"opt": "-x", "args": []})
    else:
        match pOpts[0]:
            case "-h" | "--help":
                opts.append({"opt": "-h", "args": []})
            case "-u" | "--username":
                if len(pOpts) > 1:
                    opts.append({"opt": "-u", "args": [pOpts[1]]})
            case _:
                print(f"Unknown option '{pOpts[0]}'. See login --help. Aborting login.")
                opts.append({"opt": "-x", "args": []})

    return opts

def getUsername() -> str:
    '''
    Prompts the user for a username.

    Args:
        None:   No arguments.

    Returns:
        str:    String containing username as entered by user, including spaces.
    '''
    uname = input("Username: ")
    return uname

def getPassword() -> str:
    '''
    Uses the getpass module to prompt the user for a password while not printing
    the input to the terminal.

    Args:
        None:   No arguments.

    Returns:
        str:    String containing password as entered by user, including spaces.
    '''
    pw = getpass.getpass("Password: ")
    return pw

def buildRequestBody(uname:str, pw: str) -> dict[str, str]:
    '''
    Builds the body of the POST request that will be sent to the SFC server.

    Args:
        uname (str):    The username provided, including any spaces.
        pw (str):       The password provided, including any spaces.
    
    Returns:
        dict(str, str): Dictionary to be used for the request body.
    '''
    body = {}
    body["login"] = uname
    body["password"] = pw
    body["commit"] = "Sign In"
    return body

def buildRequestHeaders() -> dict[str, str]:
    '''
    Builds the POST request headers to be send to the SFC server.

    Args:
        None:   No arguments.

    Returns:
        dict(str, str): Dictionary containing the headers as pairs of strings.
    '''
    headers = {}
    headers["Accept"] = "text/html"
    headers["Accept-Language"] = "en-CA,en-US"
    headers["Upgrade-Insecure-Requests"] = "1"
    return headers

def optHelp():
    '''
    Prints help text for login command to the terminal.

    Args:
        None:   No arguments.

    Returns:
        None:   No returned objects.
    '''
    w = shutil.get_terminal_size().columns
    print("Usage: login [OPTION]...")
    t = "Log into the SFC server using provided username (username will be " \
        "requested by default)."
    s = textwrap.wrap(t,w)
    for l in s: print(l)
    print("\nMandatory arguments to long options are also mandatory for short options.")
    print("    -u, --username      player username (including any spaces)")
    print("    -h, --help          display this help and exit")
    print("\nExamples:")
    print("    login               will prompt for username and password")
    print("    login -u Joe        will login using username 'Joe' and will\n" \
          "                        prompt for password")
    print("    login --username    will prompt for username, since no argument\n" \
          "                        was supplied to the --username option")
