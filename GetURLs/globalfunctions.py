# Set of functions commonly used by the module.
__all__ = [
    "ObsolescenceError", "GetResponse", "GetSoup", "GetJson", "EvalSoup",
    "StartAndPages"]

import json
from bs4 import BeautifulSoup
from cfscrape import create_scraper
from requests import ConnectionError, ReadTimeout
from requests.models import Response
from time import sleep

class ObsolescenceError(Exception):
    pass

def GetResponse(URL: str, method: str, **args) -> Response:
    """Gets a response (object type Response) from the requested URL. The first
    argument is the page URL, the second the method to use, the valid values
    are: "GET" and "POST", and the other arguments are the same as those of the
    "get" or "post" function of the "Requests" module. If the timeout is not
    specified, it will be set to ten seconds.
    """

    if "timeout" not in args:
        args['timeout'] = 10

    attempts = 3

    while attempts > 0:
        response = create_scraper()

        try:
            if method == "GET":
                return response.get(URL, **args)
            elif method == "POST":
                return response.post(URL, **args)
            else:
                raise ValueError(
                    f'"{method}" is not a valid method, use "GET" or "POST" as'
                    ' possible values.')

        except (ConnectionError, ReadTimeout) as e:
            response.close()
            attempts -= 1
            if attempts == 0: raise e

        sleep(1)

def GetSoup(URL: str, method: str = "GET", **args) -> BeautifulSoup:
    """This function returns an object of type "BeatifulSoup" with the
    entered URL which can be a string or an object of type "Response".
    """

    if type(URL) == str:
        URL = GetResponse(URL, method, **args)
    elif type(URL) != Response:
        raise TypeError('URL must be a string or object of type "Response".')

    out = BeautifulSoup(URL.content, "html.parser")
    URL.close()
    return out

def GetJson(data: str) -> dict:
    """Gets the data contained in a JSON.
    """

    return json.loads(data)

def EvalSoup(soup: BeautifulSoup):
    """Checks if the variable passed as argument is None, and if it is, throws
    an exception.
    """

    if soup is None:
        raise RuntimeError(
            "The data necessary to obtain the URLs could not be obtained.")

def StartAndPages(start: int, pages: int, n_elements: int):
    if start > n_elements: start = n_elements
    if (pages == 0) or (start+pages > n_elements): pages = n_elements + 1
    else: pages = start + pages
    if start == pages: pages += 1

    return start, pages
