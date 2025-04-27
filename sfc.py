#!/usr/bin/env python3

import requests
import os
from html.parser import HTMLParser

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

if __name__ == "__main__":
    s = requests.Session()
    url = "https://playstarfleet.com/login"
    try:
        r = sendGetRequest(url, None, s)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except requests.RequestException as err:
        print(f"Request error: {err}")
    except ValueError as err:
        print(f"Error: {err}")
    
    if r: print(r.text[:59])

    exit()
