#!/usr/bin/env python3

import requests
import getpass
from bs4 import BeautifulSoup
import re

def sendGetRequest(url:str, params:dict=None, s:requests.Session=None) -> requests.Response:
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

def sendPostRequest(url:str, body:dict, hdrs:dict, s:requests.Session=None) -> requests.Response:
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
    s = lc.find("h1").get_text().strip() + "\n"
    s = s + lc.find("p").get_text().strip() + "\n"
    for item in lc.find_all("li"):
        s = s + "• " + re.sub(r"\s{2,}", "", item.get_text().strip()) + "\n"
    return s

def getMainMenu() -> str:
    s = "=========================\n"
    s = s + "\033[1m   STARFLEET COMMANDER\033[0m\n"
    s = s + "   Terminal Interface\n"
    s = s + "=========================\n"
    s = s + "\nMAIN MENU\n"
    s = s + "---------\n"
    s = s + "1. Log in\n"
    s = s + "2. Exit\n"
    return s

if __name__ == "__main__":
    # Start session and get login page.
    s = requests.Session()
    url = "https://playstarfleet.com/login"
    try:
        #r = sendGetRequest(url, None, s)
        pass
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}\nExiting...")
        exit()
    except requests.RequestException as err:
        print(f"Request error: {err}\nExiting...")
        exit()
    except ValueError as err:
        print(f"Error: {err}\nExiting...")
        exit()
    
    # Display main menu and get user input.
    print(getMainMenu())
    cok = False
    while not cok:
        c = input("Command: ")
        if c in ["1", "log in", "login", "1. Log in"]:
            cok = True
            print("I'm still working on the login function.")
        elif c in ["2", "exit", "Exit", "2. Exit"]:
            print("Signing out. Goodbye!")
            exit()
        else:
            print("I didn't understand that. Please try again.")
    '''un = input("Username: ")
    pw = getpass.getpass("Password: ")'''

    exit()
