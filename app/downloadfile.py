# Code file where you have the function to download the files.

__all__ = ["DownloadFile", "RestartDownload"]

import subprocess
import sys
from os import get_terminal_size, makedirs, remove, system
from os.path import abspath, basename, exists, getsize, sep
from requests import ConnectionError, ReadTimeout, Response
from time import time

try:
    from .auxfunctions import (
        AdjustRoute, ClearName, PrintDivisor, PrintWithColor, ValueToStr,
        VerifyInternetConnection)
    from .GetURLs.globalfunctions import GetResponse
    from .langs import langs
    from .lockfile import Open

except ImportError:
    from auxfunctions import (
        AdjustRoute, ClearName, PrintDivisor, PrintWithColor, ValueToStr,
        VerifyInternetConnection)
    from GetURLs.globalfunctions import GetResponse
    from langs import langs
    from lockfile import Open

if sys.platform.startswith("win32"):
    try:
        from .gotoxy import GetCursorPosition, SetCursorPosition
    except ImportError:
        from gotoxy import GetCursorPosition, SetCursorPosition


class RestartDownload(Exception):
    """It is an exception for internal use and controlled for the sole purpose
    of restarting the download when the file is deleted after the download has
    started.
    """
    pass


def DownloadFile(
        URL: str, folder: str, lang: str, continue_downloads: bool = True,
        ignore_max_lenght: bool = True):
    # Start downloading files.

    filename = URL
    file_response = None
    local_size, online_size = None, None

    if folder == "": folder = abspath("Downloads")
    else: folder = abspath(folder)
    if not exists(folder): makedirs(folder, exist_ok=True)

    filename = ClearName(basename(URL.strip("/")))
    filename = sep.join((folder, filename))

    if len(filename) > 240 and sys.platform.startswith("win32") \
            and not ignore_max_lenght:
        temp = AdjustRoute(filename, 240)

        PrintWithColor(langs[lang]['td'].format(filename, temp), langs[lang])
        filename = temp

    def _DownloadFile():
        nonlocal file_response, local_size, online_size
        headers = {}

        file_response = _GetResponse(URL, lang)

        if "Content-Length" in file_response.headers:
            online_size = int(file_response.headers['Content-Length'])
        else:
            online_size = None

        if continue_downloads and online_size and exists(filename):
            local_size = getsize(filename)

            if local_size > online_size:
                local_size = 0
                remove(filename)

            elif local_size < online_size:
                headers = {'Range': f"bytes={local_size}-{online_size}"}

            else:
                # Informs that the file is already downloaded.
                PrintWithColor(
                    langs[lang]['tf'].format(filename[len(abspath("."))+1:]),
                    langs[lang])
                file_response.close()
                return "FINISH"

            file_response.close()

        else:
            if not online_size: online_size = "---"
            local_size = 0

            if not exists(folder): makedirs(folder, exist_ok=True)
            elif exists(filename): remove(filename)

        file_response = _GetResponse(URL, lang, headers=headers)

    if _DownloadFile() == "FINISH": return

    file = Open(filename, "ab")

    while True:
        try:
            bytes_downloaded = 0
            start = time()
            lapse = 0
            progress = ""

            # Informs which file is being downloaded now.
            PrintWithColor(
                langs[lang]['d'].format(
                    filename[len(abspath("."))+1:]), langs[lang])

            if sys.platform.startswith("win32"):
                cursor_position = GetCursorPosition()

            # Download starts or continues
            for chunk in file_response.iter_content(chunk_size=1024):
                if not exists(filename):
                    raise RestartDownload("Restart download.")
                else:
                    file.Write(chunk)

                bytes_downloaded += len(chunk)
                local_size += len(chunk)

                if lapse >= 1.0:
                    progress = \
                        f"{langs[lang]['si']} {ValueToStr(local_size)} /" \
                        + f" {ValueToStr(online_size)} | {langs[lang]['sp']}" \
                        + f" {ValueToStr(bytes_downloaded)}/s     "

                    # Informs the progress of the download.
                    if sys.platform.startswith("win32"):
                        SetCursorPosition(*cursor_position)
                        PrintWithColor(progress, langs[lang])

                    else:
                        columns = get_terminal_size()[0]

                        if (len(progress) > columns) and (columns-3 > 0):
                            progress = progress[0:columns-3] + "..."

                        PrintWithColor(progress, langs[lang], end="\r")
                        sys.stdout.flush()

                    bytes_downloaded = 0
                    start = time()

                lapse = time() - start

            file.Close()

            if bytes_downloaded != 0:
                if lapse != 0.0:
                    bytes_downloaded = bytes_downloaded * 100 / (lapse*100)
                else:
                    bytes_downloaded = 0

                progress = \
                    f"{langs[lang]['si']} {ValueToStr(local_size)} /" \
                    + f" {ValueToStr(online_size)} | {langs[lang]['sp']}" \
                    + f" {ValueToStr(bytes_downloaded)}/s     "

                # Informs the progress of the download.
                if sys.platform.startswith("win32"):
                    SetCursorPosition(*cursor_position)
                    PrintWithColor(progress, langs[lang])

                else:
                    columns = get_terminal_size()[0]

                    if (len(progress) > columns) and (columns-3 > 0):
                        progress = progress[0:columns-3] + "..."

                    PrintWithColor(progress, langs[lang], end="\r")
                    sys.stdout.flush()

            # Informs that the file has been downloaded.
            if not sys.platform.startswith("win32"):
                PrintWithColor(progress, langs[lang])

            PrintWithColor(
                langs[lang]['hb'].format(filename[len(abspath("."))+1:]),
                langs[lang])

            return

        except ConnectionError:
            file_response.close()

            while not VerifyInternetConnection():
                # Informs that there is no internet connection.
                PrintWithColor(langs[lang]['ni'], langs[lang])

            if online_size != "---":
                local_size = getsize(filename)
                headers = {'Range': f"bytes={local_size}-{online_size}"}
                file_response = _GetResponse(URL, lang, headers=headers)

            else:
                file_response = _GetResponse(URL, lang)
                if exists(filename): remove(filename)

            continue

        except RestartDownload:
            file.Close()
            file_response.close()

            # Informs that the download will have to be restarted.
            PrintWithColor(langs[lang]['tfao'], langs[lang])

            makedirs(folder, exist_ok=True)

            file = Open(filename, "ab")
            _DownloadFile()

        except (BaseException, Exception) as exception:
            file.Close()
            file_response.close()
            raise exception

def _GetResponse(URL: str, lang: str, **args) -> Response:
    # Returns an object of type Response of the URL passed as argument.
    while True:
        try:
            return GetResponse(URL, stream=True, **args)

        except (ConnectionError, ReadTimeout):
            while not VerifyInternetConnection():
                PrintWithColor(langs[lang]['ni'], langs[lang])
