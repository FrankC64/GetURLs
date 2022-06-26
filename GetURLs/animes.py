# Scraping is only available for pages oriented to anime.
__all__ = ["SupportIsAvailable", "AnimesYield", "Animes"]

import re
import time
from requests import ConnectionError, ReadTimeout
from .globalfunctions import *

supported = ("jkanime.net",)

def SupportIsAvailable(URL: str) -> bool:
    """Check if there is support for the given URL.
    """

    for sup in supported:
        if sup in URL.lower(): return True
    return False

def AnimesYield(URL: str, start: int = 1, pages: int = 0) -> dict:
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

    if "jkanime.net" in URL.lower():
        soup = GetSoup(URL, "GET")

        if soup.find("img", attrs={'alt': "Error 404"}):
            raise RuntimeError("The given URL is invalid.")

        name = soup.find("title").text
        name = name[:name.find(" - anime")]

        n_caps = soup.findAll("a", attrs={'class': "numbers"})

        # Eval if is None.
        EvalSoup(n_caps)

        n_caps = int(n_caps[-1].text[n_caps[-1].text.find("- ")+2:])

        start, pages = StartAndPages(start, pages, n_caps)

        yield {'INFO': {
            'name': name, 'start': start, 'pages': pages - start}}

        base_URL = soup.find("meta", attrs={'property': "og:url"})["content"]

        for n_cap in range(start, pages):
            soup = GetSoup(f"{base_URL}{n_cap}/", "GET")

            capitule = soup.find(
                "div", attrs={'class': "breadcrumb__links"})
            try: EvalSoup(n_caps)
            except RuntimeError: continue

            capitule = soup.find("h1")
            try: EvalSoup(n_caps)
            except RuntimeError: continue

            soup = [
                script for script in soup.findAll("script")
                if "var video = [];" in str(script)]

            URLs = re.findall(r'(?:src=")(.*?)(?:")', soup[0].text)
            temp_URLs = {}

            for URL_filter in URLs:
                if "jk.php" in URL_filter: temp_URLs[0] = URL_filter
                elif "jkvmixdrop.php" in URL_filter: temp_URLs[2] = URL_filter
                elif "jkokru.php" in URL_filter: temp_URLs[1] = URL_filter
                elif "jkfembed.php" in URL_filter: temp_URLs[3] = URL_filter
                elif "um.php" in URL_filter: temp_URLs[4] = URL_filter

            URLs = dict(sorted(temp_URLs.items()))

            for URL in URLs.values():
                if not URL.startswith("https://jkanime.net"):
                    URL = "https://jkanime.net" + URL

                if "jk.php" in URL:  # Xtreme S
                    # NOTE: Best supplier.

                    soup = GetSoup(
                        URL, "GET", headers={'referer': f"{base_URL}{n_cap}/"})

                    out = re.findall(r"(?:url: ')(.*?)(?:')", str(soup))
                    try: EvalSoup(out)
                    except RuntimeError: continue

                    yield {capitule.text: {'file': out, 'server': "Xtreme S"}}
                    break

                elif "jkvmixdrop.php" in URL:  # MixDrop
                    # NOTE: Sometimes the link to the video cannot be obtained.

                    soup = GetSoup(
                        URL, "GET", headers={'referer': f"{base_URL}{n_cap}/"})

                    soup = GetSoup(
                        "https:" + soup.find("iframe")['src'], "GET")

                    try:
                        delivery = re.findall(
                            r'(?:MDCore\|\|)(.*?)(?:\|[0-9]{0,})',
                            str(soup))[0]
                        out = re.findall(
                            r'(?:delivery[0-9]{0,}\|)(.*?)(?:\|vfile)',
                            str(soup))

                    except IndexError:
                        continue

                    out = out[0].replace("|mxdcontent|", ".")
                    out = out.replace("|net|referrer|", "?s=")
                    out = out.replace(
                        "|thumbs||jpg|furl|wurl||v|s|_t|", "&e=")
                    out = \
                        f"https://a-{delivery}.mxdcontent.net/v/" \
                        + out.replace("|", "&_t=")

                    yield {capitule.text: {'file': [out], 'server': "MixDrop"}}
                    break

                elif "jkokru.php" in URL:  # Okru
                    # NOTE: Sometimes videos are banned.

                    soup = GetSoup(
                        URL, "GET", headers={'referer': f"{base_URL}{n_cap}/"})

                    soup = soup.find("iframe")
                    try: EvalSoup(soup)
                    except RuntimeError: continue

                    soup = GetSoup(soup['src'], "GET")

                    if "blocked" in str(soup):
                        continue

                    re_exp = (
                        r"https://vd[0-9]{0,}\.mycdn\.me/\?expires=\d+\\\\"
                        r"[0-9a-zA-Z]{0,}=\d+\.\d+\.\d+\.\d+\\\\"
                        r"[0-9a-zA-Z]{0,}=\d+\\\\[0-9a-zA-Z]{0,}=[A-Z\_]{0,}"
                        r"\\\\[0-9a-zA-Z]{0,}=\d+\.\d+\.\d+\.\d+\\\\"
                        r"[0-9a-zA-Z]{0,}=\d+\\\\[0-9a-zA-Z]{0,}="
                        r"[0-9a-zA-Z\-\_]{0,}\\\\[0-9a-zA-Z]{0,}=\d+\\\\"
                        r"[0-9a-zA-Z]{0,}=\d+\.\d+\.\d+\.\d+\\\\"
                        r"[0-9a-zA-Z]{0,}=\d+\\\\[0-9a-zA-Z]{0,}=\d+"
                    )

                    soup = soup.find("div", attrs={'data-module': "OKVideo"})
                    try: EvalSoup(soup)
                    except RuntimeError: continue

                    with open("a.txt", "w") as f:
                        f.write(soup['data-options'])

                    soup = re.findall(re_exp, soup['data-options'])

                    if ("type=1" in soup[-1]) and (len(soup) > 1):
                        out = soup[-2].replace("\\\\u0026", "&")
                    else:
                        out = soup[-1].replace("\\\\u0026", "&")

                    yield {capitule.text: {'file': out, 'server': "Okru"}}
                    break

                elif "jkfembed.php" in URL:  # Fembed
                    # NOTE: Denies requests when there are many requests.

                    soup = GetSoup(
                        URL, "GET", headers={'referer': f"{base_URL}{n_cap}/"})

                    headers = {'referer': soup.find("iframe")['src']}
                    post = headers['referer'].replace(
                        "https://www.fembed.com/v",
                        "https://suzihaza.com/api/source")

                    attempts = 3
                    while attempts > 0:
                        out = GetSoup(post, "POST", headers=headers)

                        if out.find("center") is None:
                            out = re.findall(
                                r'(?:{"file":")(.*?)(?:",)', str(out))

                            out = out[-1].replace("\\", "")
                            break

                        else:
                            # Waiting time for Fembed not to deny the request.
                            attempts -= 1
                            for i in range(10): time.sleep(0.1)

                    else:
                        continue

                    yield {capitule.text: {'file': [out], 'server': "Fembed"}}
                    break

                elif "um.php" in URL:  # Desu
                    # NOTE: Returns many links.

                    soup = GetSoup(
                        URL, "GET", headers={'referer': f"{base_URL}{n_cap}/"})

                    out = GetResponse(
                        re.findall(r"(?:swarmId: ')(.*?)(?:')", str(soup))[0],
                        "GET")

                    out = re.findall(r"(?:,\n)(.*?)(?:\n#)", out.text)

                    yield {capitule.text: {'file': out, 'server': "Desu"}}
                    break

            else:
                yield {capitule.text: "No compatible providers were found."}

def Animes(URL: str, start: int = 1, pages: int = 0) -> dict:
    """Exactly the same as "AnimesYield" with the difference that this function
    waits to have the information and all the pages to be returned.
    """

    out = {}
    for item in AnimesYield(URL, start, pages): out.update(item)
    return out
