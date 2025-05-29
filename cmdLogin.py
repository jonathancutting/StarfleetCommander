import requests
import getpass

def login(p:str, s:requests.Session):
    pStr = p.split(" ")
    if len(pStr) == 1:
        cmdLogin(s)

def cmdLogin(s:requests.Session):
    loc = "https://playstarfleet.com/login/authenticate"
    body = {}
    hdrs = {}

    # Build request body.
    uname = input("Username: ")
    body["login"] = uname
    passwd = getpass.getpass("Password: ")
    body["password"] = passwd
    body["commit"] = "Sign In"

    # Build request headers.
    hdrs["Accept"] = "text/html"
    hdrs["Accept-Language"] = "en-CA,en-US"
    hdrs["Upgrade-Insecure-Requests"] = "1"

    print(body)
    print(hdrs)
    #resp = sendPostRequest(loc, body, hdrs, s)