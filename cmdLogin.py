import requests
import getpass
import shutil
import textwrap

def login(cmd:dict, s:requests.Session):
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

def parseArgs(pOpts:list[str]) -> list:
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
    uname = input("Username: ")
    return uname

def getPassword() -> str:
    pw = getpass.getpass("Password: ")
    return pw

def buildRequestBody(uname:str, pw: str) -> dict:
    body = {}
    body["login"] = uname
    body["password"] = pw
    body["commit"] = "Sign In"
    return body

def buildRequestHeaders() -> dict:
    headers = {}
    headers["Accept"] = "text/html"
    headers["Accept-Language"] = "en-CA,en-US"
    headers["Upgrade-Insecure-Requests"] = "1"
    return headers

def optHelp():
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
