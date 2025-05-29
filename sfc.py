#!/usr/bin/env python3

import os                           # for file system and terminal commands
import requests                     # for REST requests
import getpass                      # to allow non-printing input
from bs4 import BeautifulSoup       # HTML parser
import re                           # for regular expression processing
import textwrap                     # to make text in terminal look pretty
import shutil                       # to get information about terminal

import cmdLogin

class FCOLOR:
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINKING = "\033[5m"
    STRIKETHROUGH = "\033[9m"

def sendGetRequest(url:str, params:dict, s:requests.Session) -> requests.Response:
    '''
    Sends a GET request to the specified URL and returns response object.
    If URL is invalid, or request is unsuccessful, an an error is raised.

    Args:
        url (str): location to send the GET request
        params (dict, optional): headers to send with the request
        s (requests.Session, optional): Session object to manage headers

    Returns:
        requests.response: HTML response object
    '''
    if not url: raise ValueError("URL cannot be empty.")
    try:
        if not s:
            r = requests.get(url, params=params)
        else:
            r = s.get(url, params=params)
        r.raise_for_status() # Raise exception for 4xx and 5xx status codes.
        return r
    except:
        raise

def sendPostRequest(url:str, body:dict, hdrs:dict, s:requests.Session) -> requests.Response:
    '''
    Sends a POST request to the specified URL and returns the response object.
    If URL is invalid, or request is unsuccessful, then an error is raised.

    Args:
        url (str): location to send the POST request
        body (dict): information to send to the remote server
        hdrs (dict): header information to include in the request
        s (requests.Session, optional): Session object to manage headers

    Returns:
        requests.response: HTML response object
    '''
    if not url: raise ValueError("URL cannot by empty.")
    try:
        if not s:
            r = requests.post(url, data=body, headers=hdrs)
        else:
            r = s.post(url, data=body, headers=hdrs)
        r.raise_for_status() # Raise exception for 4xx and 5xx status codes.
        return r
    except:
        raise

def clearConsole():
    if os.name == "nt":     # for Windows
        os.system("cls")
    else:                   # for Linux/Mac
        os.system("clear")

def getWelcomeMessage(htm:bytes) -> str:
    '''
    Uses BeautifulSoup to extract the welcome message from the login page and
    returns a formatted string.

    Args:
        htm (bytes): the requests.response object content containing html

    Returns:
        str: string containing a formatted version of the welcome message
    '''
    soup = BeautifulSoup(htm, "html.parser")
    lc = soup.find(id="leftColumn")
    s = lc.find("h1").get_text().strip() + "\n"                    #type: ignore
    s = s + lc.find("p").get_text().strip() + "\n"                 #type: ignore
    for item in lc.find_all("li"):                                 #type: ignore
        s = s + "• " + re.sub(r"\s{2,}", "", item.get_text().strip()) + "\n"
    return s

def getMainMenu() -> str:
    s = "=========================\n"
    s = s + "\033[1m   STARFLEET COMMANDER\033[0m\n"
    s = s + "=========================\n"
    s = s + "\nMAIN MENU\n"
    s = s + "---------\n"
    s = s + "1. Log in\n"
    s = s + "8. Switch to terminal mode\n"
    s = s + "9. Exit\n"
    return s

def cmdHelp():
    s = []
    w = shutil.get_terminal_size().columns
    t = "Starfleet Commander Terminal Mode functions in much the same way " \
     "as the terminal in Linux does. At the command prompt, you type a command " \
     "you want to perform, along with any options relevant to that command."
    s.append(textwrap.fill(t, w))
    
    t = "For example, from the prompt \"sfc:~$\", you might type \"planets\" to " \
     "view a list and description of your planets. Similarly, you might type " \
     "\"fleet\" to view your current fleet status."
    s.append(textwrap.fill(t, w))

    t = "You can also add options to these commands, if the command supports them. " \
     "For example, \"sfc:~$ galaxy -g8 -s35\" will run the galaxy command with " \
     "options g8 and s35, and you will be shown information for System 35 in " \
     "Galaxy 8."
    s.append(textwrap.fill(t, w))

    t = "For help with a specific command or to see its available options, type " \
     "the command followed by \"--help\"."
    s.append(textwrap.fill(t, w))

    t = "Current commands are: login, help, exit, quit"
    s.append(textwrap.fill(t, w))
    
    for l in s:
        print(l, "\n")

def buildCommandDict(s:str) -> dict:
    '''
    Builds a simple command dictionary to send to the relevant command module.
    
    Args:
        s (str): contains the command and all options/arguments. The string
           will be split using a space as the delimiter. The first substring
           is assumed to be the command, and all subsequent substrings are
           placed into a list for the dictionary's "args" element.
    Returns:
        dict: dictionary containing two elements. The "cmd" element contains the
              command as a string, and the "args" element is a list containing
              everything else.
    '''
    cmdDict = {}
    cmdDict["cmd"] = ""
    cmdDict["args"] = []
    spl = s.split(" ")

    if len(spl) == 1:               # passed string has only one substring
        cmdDict["cmd"] = spl[0]
    elif len(spl) > 1:              # passed string has more than one substring
        cmdDict["cmd"] = spl[0]
        for a in spl[1:]:
            cmdDict["args"].append(a)
    return cmdDict

if __name__ == "__main__":
    # Start session and get login page.
    s = requests.Session()
    url = "https://playstarfleet.com/login"
    try:
        print("Trying to connect to SFC...")
        r = sendGetRequest(url, {}, s)
        # print(getWelcomeMessage(r.content))
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}\nExiting...")
        exit()
    except requests.RequestException as err:
        print(f"Request error: {err}\nExiting...")
        exit()
    except ValueError as err:
        print(f"Error: {err}\nExiting...")
        exit()
    
    # Start terminal interface.
    clearConsole()
    print(f"   {FCOLOR.BOLD}STARFLEET COMMANDER - Terminal Interface{FCOLOR.RESET}")
    print("==============================================")
    go = True
    while go:
        c = input(f"{FCOLOR.BOLD}{FCOLOR.GREEN}sfc{FCOLOR.DEFAULT}:{FCOLOR.BLUE}~{FCOLOR.DEFAULT}${FCOLOR.RESET} ")
        cmdDict = buildCommandDict(c)
        match cmdDict["cmd"]:
            case "login":
                cmdLogin.login(cmdDict, s)
                #print(s.auth)
            case "exit" | "quit":
                go = False
            case "help":
                cmdHelp()
            case "":
                pass
            case _:
                print(f"Command '{cmdDict['cmd']}' not found. See 'help' for a list of available commands.")

    print("Signing out. Goodbye!")
    exit()
