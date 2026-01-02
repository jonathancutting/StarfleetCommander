import requests                         # to handle REST exceptions
import getpass                          # to obfuscate password while typing
import shutil                           # to get terminal window properties
import textwrap                         # to gracefully wrap text in terminal
import logging                          # built-in Python logging
from restRequests import sendRequest    # to send REST requests

logger = logging.getLogger(__name__)    # set module-level logging object

def login(cmd:dict[str, list[str]], s:requests.Session) -> str:
    '''
    Handles the "login" command from sfc main function.

    :param cmd: Dictionary of the user-entered command string, as parsed by the
                buildCommandDict function in sfc.py. The dictionary should
                contain two elements: first, a string with the command, and
                secondly, a list of strings with the arguments.
    :type cmd:  dict[str, list[str]]

    :param s:   The user's request session object.
    :type s:    requests.Session

    :return:    If the login was successful, the function will return a string
                containing the HTML text of the returned page.
                If the login was unsuccessful, the function will return an empty
                string, and an error message may be printed to the console.
    :rtype:     str
    '''

    logger.debug("Entered function %(funcName)s.")
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
                return ""
            case "-u":
                if len(opts[0]["args"]) > 0:
                    uname = opts[0]["args"][0]
                else:
                    uname = getUsername()
                pw = getPassword()
            case "-x":
                return ""
            case _:
                logger.info("Unknown option supplied for login: %s.", opts[0]['opt'])
                print(f"Unknown option '{opts[0]['opt']}'. Aborting login.")
                return ""
    
    headers = buildRequestHeaders()
    body = buildRequestBody(uname, pw)
    url = "https://playstarfleet.com/login/authenticate"
    restDict = {"url":url, "body":body, "hdr":headers, "sess":s}
    
    try:
        logger.info("Logging in...")
        response = sendRequest(restDict)
    except (requests.exceptions.HTTPError, requests.RequestException, ValueError):
        print("There was a problem logging in. Login failed.")
        logger.exception("Error encountered while attempting to log in.")
        return ""
    
    # If it gets to this point, then a response should have been received.
    # Check for successful login.
    if response.text.find("Invalid login or password") != -1:
        # Login was unsuccessful. Tell user and return empty string.
        logger.info("User supplied an invalid username or password for login.")
        print("Login failed. Invalid username or password.")
        return ""
    else:
        # Login was successful. Return repsonse HTML.
        logger.info("Login successful.")
        return response.text

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

    logger.debug("Entered function %(funcName)s.")
    opts = []

    if len(pOpts) == 0: return opts

    if pOpts[0][0] != "-":
        print("The login option you supplied is incorrect. See login --help.")
        logger.info("User supplied malformed option '%s' for login.", pOpts[0])
        opts.append({"opt": "-x", "args": []})
    else:
        match pOpts[0]:
            case "-h" | "--help":
                opts.append({"opt": "-h", "args": []})
            case "-u" | "--username":
                if len(pOpts) > 1:
                    x = pOpts[1]
                    if len(pOpts) > 2:
                        for i in range(2, len(pOpts)):
                            x = x + " " + pOpts[i]
                    opts.append({"opt": "-u", "args": [x]})
            case _:
                print("The login option you supplied is incorrect. See login --help.")
                logger.info("User supplied unknown option %s for login.", pOpts[0])
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
    Builds the POST request headers to be sent to the SFC server.

    Args:
        None:   No arguments.

    Returns:
        dict(str, str): Dictionary containing the headers as pairs of strings.
    '''
    headers = {}
    headers["Accept"] = "text/html"
    headers["Accept-Language"] = "en"
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

def logout(sess:requests.Session) -> None:
    '''
    Handles the logout command from the sfc module main function.

    Args:
        sess (requests.Session):    The user's request Session object.

    Returns:
        None:   Function does not return an object.
    '''

    logger.debug("Entered function %(funcName)s.")
    logger.info("Logging out...")
    url = "https://playstarfleet.com/login/logout"
    hdr = buildRequestHeaders()
    restDict = {"url":url, "hdr": hdr, "sess": sess}
    try:
        resp = sendRequest(restDict)
        if resp.url != "https://playstarfleet.com/login?view=login":
            logger.warning("Logout unsuccessful. Unexpected response URL.")
        else:
            logger.info("Logout successful.")
    except (requests.exceptions.HTTPError, requests.RequestException, ValueError):
        logger.exception("Error encountered while trying to log out.")
