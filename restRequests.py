import requests

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

def sendRequest(req:dict) -> requests.Response:
    '''
    Takes a generic request object and interprets it to determine which REST
    function should be called. Checks first that request dictionary is properly
    formed. Any errors raised by REST functions are passed to caller.

    Args:
        req (dict): dictionary containing the following keys:
            url (str): the URL of the request target
            sess (requests.Session): the current requests session object
            hdr (dict): dictionary containing the request headers. If missing,
                        an empty dictionary will be created for it.
            body (dict, opt): dictionary containing the request body, optional
                              if making a GET request

    Returns:
        requests.Response: HTML response object
    '''

    # Raise error, if necessary members are missing.
    if not "url" in req:
        raise ValueError("URL is missing from request!")
    if not "sess" in req:
        raise ValueError("Session object is missing from request!")
    
    # Prepare empty header dictionary, if missing.
    if not "hdr" in req:
        req["hdr"] = {}

    # Detect appropriate request function and make call. Propogate any errors to caller.
    try:
        if not "body" in req:
            r = sendGetRequest(req["url"], req["hdr"], req["sess"])
        else:
            r = sendPostRequest(req["url"], req["body"], req["hdr"], req["sess"])
    except:
        raise

    return r