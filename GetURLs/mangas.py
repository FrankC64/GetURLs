# Scraping is only available for pages oriented to mangas and manwhas.
__all__ = ["SupportIsAvailable", "MangasYield", "Mangas"]

import re
from requests import ConnectionError, ReadTimeout
from .globalfunctions import (
    EvalSoup, GetJson, GetResponse, GetSoup, StartAndPages)

supported = ("novelcool.com",)

def SupportIsAvailable(URL: str) -> bool:
    """Check if there is support for the given URL.
    """

    for sup in supported:
        if sup in URL.lower(): return True
    return False

def MangasYield(URL: str, start: int = 1, pages: int = 0) -> dict:
    """It obtains the information and URLs from the given URL and returns them
    periodically. The first return will always be a dictionary with data such
    as name, start and number of pages, and then it will return the URLs per
    page.
    """

    if not SupportIsAvailable(URL):
        yield {}
        return

    if not URL.lower().startswith("https://") and \
            not URL.lower().startswith("http://"):
        URL = "https://" + URL

    if start < 1: start = 1
    if pages < 0: pages = 0

    if "novelcool.com" in URL.lower():
        if "es.novelcool.com" in URL:
            headers = {'referer': URL}
        elif "en.novelcool.com" in URL:
            headers = {'referer': "https://www.novelcool.com"}
        else:
            yield {"ERROR": "URL of noovelcool incompatible."}
            return

        soup = GetSoup(URL, "GET")
        name = soup.find("h1", attrs={'itemprop': "name"})

        if name is None:
            URL = soup.find("a")
            EvalSoup(URL)

            name = URL.find("span")

            if name is None:
                raise DeprecationWarning(
                    "Invalid URL. The expected indications are not found.")

            URL = URL['href']
            soup = GetSoup(URL, "GET")
            name = soup.find("h1", attrs={'itemprop': "name"}).text

        else:
            name = name.text

        URLs_chapter = soup.find("div", attrs={'class': "chapter-item-list"})
        URLs_chapter = URLs_chapter.findAll("a")
        URLs_chapter.reverse()

        start, pages = StartAndPages(start, pages, len(URLs_chapter))
        start -= 1; pages -= 1

        yield {'INFO': {
            'name': name, 'start': start + 1, 'pages': pages - start}}

        for i in range(start, pages):
            soup = GetSoup(URLs_chapter[i]['href'], "GET", headers=headers)
            soup = str(soup)

            URLs = re.findall(r"(?:\")(.*?)(?:\",)", soup[:soup.find("],")])
            yield {URLs_chapter[i]['title']: URLs}

    else:
        yield {}

def Mangas(URL: str, start: int = 1, pages: int = 0) -> dict:
    """Exactly the same as "MangasYield" with the difference that this function
    waits to have the information and all the pages to be returned.
    """

    out = {}
    for item in MangasYield(URL, start, pages): out.update(item)
    return out
