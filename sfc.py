#!/usr/bin/env python3

import os                           # for file system and terminal commands
import requests                     # for REST requests
from bs4 import BeautifulSoup       # HTML parser
import re                           # for regular expression processing
import textwrap                     # to make text in terminal look pretty
import shutil                       # to get information about terminal
import logging                      # built-in Python logging
import sys                          # for standard I/O

import plogger                          # for logging with fallback
from restRequests import sendRequest    # for standardized REST functionality
from cmdLogin import login, logout      # for login and logout commands

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

def main():
    # Configure the logger.
    plogger.configRootLogger()
    logger = logging.getLogger(__name__)
    logger.info("Application started.")

    # Start session and get login page.
    s = requests.Session()
    url = "https://playstarfleet.com/login"
    try:
        print("Trying to connect to SFC...")
        r = sendRequest({"url": url, "sess":s})
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
    print(getWelcomeMessage(r.content.decode()))
    print()
    print(f"   {FCOLOR.BOLD}STARFLEET COMMANDER - Terminal Interface{FCOLOR.RESET}")
    print("==============================================")
    username = "" # blank until login
    path = "~"    # userhome until login
    go = True     # to start, but ensure this is set to false to break loop!
    while go:
        prompt = getPrompt(username, path)
        c = input(prompt)
        cmdDict = buildCommandDict(c)
        match cmdDict["cmd"]:
            case "login":
                rtnStr = login(cmdDict, s)
                if len(rtnStr) > 0:
                    username = getUsername(rtnStr)
                    path = "~/getbent"
            case "exit" | "quit" | "logout":
                logout(s)
                go = False
            case "help":
                r = cmdHelp()
            case "":
                pass
            case _:
                print(f"Command '{cmdDict['cmd']}' not found. See 'help' for a list of available commands.")

    print("Thank you for playing. Goodbye!")
    exit()

def clearConsole():
    if os.name == "nt":     # for Windows
        os.system("cls")
    else:                   # for Linux/Mac
        os.system("clear")

def getWelcomeMessage(htm:str) -> str:
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
     "as the terminal in Linux. At the command prompt, you type a command " \
     "you want to perform, along with any desired options supported by that command."
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
     "the command followed by \"--help\" or \"-h\"."
    s.append(textwrap.fill(t, w))

    t = "Currently supported commands are: login, help, exit, quit"
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

def getPrompt(username:str, path:str) -> str:
    '''
    Builds the terminal string that prompts user for a command. The string is of
    the form "[user@]sfc:[path]$". Before login, this is as simple as "sfc:~$",
    but after login, the username and path will be filled in. The string is also
    colour-coded to mimic the Ubuntu 22.05 terminal.

    Args:
        username (str): contains the username. If the user has not logged in
                        yet, this will be empty.
        path (str): contains the current path of the user. For example, if the
                    user is viewing the fleet page, it will be "fleet". If the
                    user is viewing the planet page, it will be
                    "planets/[planetname]".
    Returns:
        str: string containing the full, colour-coded command prompt.
    '''

    if len(path) == 0: path = "~"
    if len(username) == 0:
        prompt = f"{FCOLOR.BOLD}{FCOLOR.GREEN}sfc{FCOLOR.DEFAULT}:" \
                 f"{FCOLOR.BLUE}{path}{FCOLOR.DEFAULT}${FCOLOR.RESET} "
    else:
        prompt = f"{FCOLOR.BOLD}{FCOLOR.GREEN}{username}@sfc{FCOLOR.DEFAULT}:" \
                 f"{FCOLOR.BLUE}{path}{FCOLOR.DEFAULT}${FCOLOR.RESET} "

    # "{FCOLOR.BOLD}{FCOLOR.GREEN}sfc{FCOLOR.DEFAULT}:{FCOLOR.BLUE}~{FCOLOR.DEFAULT}${FCOLOR.RESET} "
    return prompt

def getUsername(htm:str) -> str:
    '''
    Finds and returns the username from the passed HTML string. This function
    expects the HTML string to be the REST response containing the "home" page
    of a planet. Function uses BeautifulSoup to make the HTML parsing easier.

    Args:
        htm (str): HTML string containing a planet's "home" page. Passing a
                   different page will cause an error or undefined behaviour.
    
    Returns:
        str: The username string. If the username isn't found, an empty string
             is returned.
    '''
    uname = ""
    soup = BeautifulSoup(htm, "html.parser")
    # Find the div elements with class "right_column". There should be only one.
    div = soup.find_all('div', class_='right_column')
    if not div is None: # Check that the div was found.
        a = div[0].find_all('a') # We want the first (and only) div.
        if not a is None: # Again, check that an anchor was found.
            uname = a[0].get_text() # We're looking for the first anchor.
    return uname

def getPath(htm:str) -> str:
    '''
    Finds and returns the path from the passed HTML string. Function uses
    BeautifulSoup to make the HTML parsing easier.

    Args:
        htm (str): HTML string. This can be any HTML page from SFC, except the
                   site homepage.

    Returns:
        str: The path string. If the path isn't found, an empty string is
             returned.
    '''
    path = ""
    soup = BeautifulSoup(htm, "html.parser")
    titleElem = soup.title
    if titleElem:       # Check that the title element exists.
        titleStr = titleElem.string
        if titleStr:    # Check that the title actually contains text.
            titles = titleStr.split(" - ")
        else:
            return ""
    else:
        return ""

    return path

if __name__ == "__main__":
    main()