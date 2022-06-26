# Module for obtaining links to multimedia files of series, mangas, etc.
__author__ = "Frank Cedano <frankcedano64@gmail.com>"
__version__ = "0.2"

__all__ = ["SupportIsAvailable", "GetURLsYield", "GetURLs"]

from . import animes, mangas

supported = {
    'Animes': animes.supported,
    'Mangas': mangas.supported,
}

support_functions = (animes.SupportIsAvailable, mangas.SupportIsAvailable)
yield_functions = (animes.AnimesYield, mangas.MangasYield)
functions = (animes.Animes, mangas.Mangas)

def SupportIsAvailable(URL: str) -> bool:
    """Check if there is support for the given URL.
    """

    for func in support_functions:
        if func(URL): return True
    return False

def GetURLsYield(URL: str, start: int = 1, pages: int = 0) -> dict:
    """It obtains the information and URLs from the given URL and returns them
    periodically. The first return will always be a dictionary with data such
    as name, start and number of pages, and then it will return the URLs per
    page.
    """

    if not SupportIsAvailable(URL):
        yield {}
        return

    close = False

    for func in yield_functions:
        for item in func(URL, start, pages):
            if item != {}: close = True; yield item

        if close: return

def GetURLs(URL: str, start: int = 1, pages: int = 0) -> dict:
    """Exactly the same as "GetURLsYield" with the difference that this
    function waits to have the information and all the pages to be returned.
    """

    for func in functions:
        for items in func(URL, start, pages):
            if items != {}: return items
