# Code file with different functions for specific tasks.
__all__ = [
    "AdjustRoute", "ClearConsole", "ClearName", "PrintDivisor", "PrintCenter",
    "PrintWithColor", "IntputWithColor", "DefaultColor",
    "VerifyInternetConnection"]

from cfscrape import create_scraper
from os import get_terminal_size, makedirs, path, system
from os.path import abspath, exists, join, sep, splitdrive, splitext
from requests import ConnectionError, ReadTimeout
from sys import platform, stdout
from time import sleep, time

if platform.startswith("win32"):
    def AdjustRoute(route: str, length: int = 240, n_elements: int = 1) -> str:
        """route: A string of the route to reduce.
        length: Maximum length that the route must have.
        n_elements: Number of elements (file and folders) that can be
        shortened.
        """

        route = abspath(route)
        if len(route) <= length: return route

        drive, rest = splitdrive(route)
        rest = rest.split(sep)

        if rest[0] == "": rest = rest[1:]
        left = len(route) - length

        for element, count in zip(reversed(rest), range(1, (len(rest)+1))):
            element = list(splitext(element))
            element_length = len(element[0])

            if n_elements is None or n_elements > 0:
                if len(element[0]) > left:
                    element[0] = element[0][:len(element[0])-left]
                    left = 0

                elif len(element[0]) < left:
                    element[0] = element[0][:1]
                    left = left - (element_length-1)

                else:
                    element[0] = element[0][:len(element[0])-left+1]
                    left = left - (element_length-1)

                rest[-count] = "".join(element)

            if n_elements is not None:
                n_elements -= 1
                if n_elements == 0 or left == 0: break

        route = sep.join(rest)

        if drive == "": return sep + route
        else: return sep.join((drive, route))

    ClearConsole = lambda: system("cls")

    # auxfunctions_winapi
    try:
        from . import auxfunctions_winapi
    except ImportError:
        import auxfunctions_winapi

elif platform.startswith("linux"):
    AdjustRoute = lambda route, length, n_elements: abspath(route)
    ClearConsole = lambda: system("clear")

def ClearName(name: str) -> str:
    """To get rid of invalid characters and words in the system.
    """

    for c in range(32): name = name.replace(chr(c), "")
    name = name.replace(chr(127), "")

    if platform.startswith("win32"):
        for c in ("<", ">", ":", '"', "/", '\\', "|", "?", "*"):
            name = name.replace(c, "_")

        for invalid_name in (
                "CON", "PRN", "AUX", "CLOCK$", "NUL", "COM0", "COM1", "COM2",
                "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT0",
                "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8",
                "LPT9"):

            if name.upper().startswith(invalid_name):
                return "NewName" + splitext(name)[1]

    else:
        name = name.replace("/", "_")

    return name

def PrintDivisor():
    """Prints a series of characters vertically with the length of the console
    in blue.
    """

    try:
        PrintWithColor("-" * (get_terminal_size()[0] - 1), color="BLUE")
    except OSError:
        PrintWithColor("-" * 10, color="BLUE")

def PrintCenter(text: str):
    """Prints the past text in the center of the current line.
    """

    try:
        space = get_terminal_size()[0] - 1

        if (space < len(text)):
            PrintWithColor(text[:space])
            PrintCenter(text[space:])

        else:
            space = " " * ((space - len(text)) // 2)
            PrintWithColor(space + text)

    except Exception:
        PrintWithColor(text)

def PrintWithColor(
        text: str, langs: dict = {}, color: str = "", end: str = "\n"):
    """Prints the string passed as the first argument with the color
    corresponding to the information found in langs or in default with the
    specified color.
    """

    if platform.startswith("win32"):
        auxfunctions_winapi.PrintWithColor(text, langs, color, end)

    else:
        if ('info' in langs) and text.startswith(langs['info']):
            print(text.replace(
                langs['info'], f"\x1B[1;33m{langs['info']}\x1B[1;37m"),
                end=end)

        elif text.startswith("ARGUMENT ERROR:"):
            print(text.replace(
                "ARGUMENT ERROR:", f"\x1B[1;31mARGUMENT ERROR:\x1B[1;37m"),
                end=end)

        elif ('error' in langs) and text.startswith(langs['error']):
            print(text.replace(
                langs['error'], f"\x1B[1;31m{langs['error']}\x1B[1;37m"),
                end=end)

        elif ('si' in langs) and text.startswith(langs['si']):
            text = text.replace(
                langs['si'], f"\x1B[1;32m{langs['si']}\x1B[1;37m")
            text = text.replace(
                langs['sp'], f"\x1B[1;32m{langs['sp']}\x1B[1;37m")
            print(text, end=end)

        else:
            if color == "BLUE":
                print("\x1B[1;34m" + text, end=end)
            else:
                print("\x1B[1;37m" + text, end=end)

def IntputWithColor(text: str, langs: dict = {}, color: str = ""):
    """It prints the passed text with color just like "PrintWithColor" and then
    it is put in standby to accept keyboard input like the "input" function.
    """

    PrintWithColor(text, langs, color, "")
    return input()

def DefaultColor():
    """Sets the terminal colors to their default state.
    """

    if platform.startswith("win32"):
        auxfunctions_winapi.DefaultColor()
    else:
        print("\x1B[0m")

def ValueToStr(value: int) -> str:
    """Converts an integer number assuming it refers to Bytes into a unit
    that can be represented in a shorter form with its respective symbol.
    """

    if value == "---": return value

    if value < 2**20: return f"{round(value / 1024, 3)}KB"
    elif value < 2**30: return f"{round(value / 1024 / 1024, 2)}MB"
    else: return f"{round(value / 1024 / 1024 / 1024, 2)}GB"

def VerifyInternetConnection() -> bool:
    """Checks if there is an internet connection, returning True if there
    is and False if not.
    """

    attempts = 3

    while attempts:
        for URL in ("https://www.google.com", "https://www.bing.com",
                    "https://www.w3.org"):
            sleep(0.5)

            try:
                response = create_scraper().get(URL)
                response.close()
                return True

            except (ConnectionError, ReadTimeout):
                pass

        attempts -= 1

    return False
