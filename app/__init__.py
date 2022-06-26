# Code file containing the program interface.
__author__ = "Frank Cedano <frankcedano64@gmail.com>"
__version__ = "1.0.1"

__all__ = ["AppClosed", "ConsoleApp", "main"]

import sys
from os import makedirs
from os.path import abspath, basename, sep
from multiprocessing import Process
from requests import ConnectionError, ReadTimeout
from threading import Thread
from time import sleep

try:
    from .auxfunctions import (
        AdjustRoute, ClearConsole, ClearName, PrintDivisor, PrintCenter,
        PrintWithColor, IntputWithColor, VerifyInternetConnection)
    from .downloadfile import DownloadFile, GetResponse
    from .GetURLs import GetURLsYield, SupportIsAvailable, supported
    from .langs import langs

except ImportError:
    from auxfunctions import (
        AdjustRoute, ClearConsole, ClearName, PrintDivisor, PrintCenter,
        PrintWithColor, IntputWithColor, VerifyInternetConnection)
    from downloadfile import DownloadFile, GetResponse
    from GetURLs import GetURLsYield, SupportIsAvailable, supported
    from langs import langs


class AppClosed(Exception):
    """Exception thrown when an error occurs that cannot be cured and indicates
    the closing of the program.
    """
    pass


class ConsoleApp:
    """Class containing the app interface.
    """

    def __init__(self):
        """Here only the variables are initialized and the arguments are
        filtered.
        """

        # Language variables.
        self.lang = "English"
        self.langs = langs[self.lang]

        # Query variables.
        self.URL = ""
        self.start = None
        self.pages = None
        self.info = {'name': "", 'folder_out': "", 'start': 0, 'pages': 0}

        # Variables for checks and validations.
        self.is_lang_selected = False
        self.info_obtaing = False
        self.continue_downloads = True
        self.ignore_max_length = False

        # Variables for download control.
        self.queue = []
        self.queue_finish = []
        self.downloaded = [0, 0]

        self.SOU_thread = Thread(target=self.StartObtainingURLs, daemon=True)

        self._FilterArgs()

        if not sys.platform.startswith("win32"):
            self.ignore_max_length = True

        if self.info['folder_out'] == "":
            self.info['folder_out'] = abspath("Downloads")

    def Start(self):
        """Method that starts the program.
        """

        ClearConsole()
        PrintCenter("---Downloader---")

        # Windows only
        if not self.ignore_max_length:
            # If the output path exceeds 180 characters the app closes.
            if len(self.info['folder_out']) > 180:
                self.PrintWithColor(
                    self.langs['tpe'].format(self.info['folder_out']))
                raise AppClosed("App closed")

        if not self.is_lang_selected:
            self.SelectLang()

        PrintDivisor()
        # Prints the language used.
        self.PrintWithColor(self.langs['ls'], self.lang)

        PrintDivisor()
        self.ObtainPreInfo()

        PrintDivisor()
        self.SOU_thread.start()
        # Informs that the URLs have already started to be obtained.
        self.PrintWithColor(self.langs['oin'])

        while self.info['name'] == "":
            sleep(0.1)
            if not self.SOU_thread.is_alive() and self.info['name'] == "":
                raise AppClosed("App closed")

        # Informs the name of the series.
        self.PrintWithColor(self.langs['sn'].format(self.info['name']))

        # Prints the name of the output folder.
        self.PrintWithColor(self.langs['f'].format(self.info['folder_out']))

        if self.start != self.info['start']:
            """Here you are informed if there have been changes in the start
            page chosen by the user.
            """
            self.PrintWithColor(
                self.langs['st'].format(self.start, self.info['start']))
            self.start = self.info['start']

        if self.pages != self.info['pages']:
            """Here you are informed if there have been changes in thenumber
            of pages selected by the user.
            """
            self.PrintWithColor(
                self.langs['pa'].format(self.pages, self.info['pages']))
            self.pages = self.info['pages']

        PrintDivisor()
        self.PreparedFiles()

    def PreparedFiles(self):
        """Prepare the files to download.
        """

        self.downloaded = [1, self.pages]
        subprocess = None

        while self.SOU_thread.is_alive() or self.queue != []:
            sleep(0.1)

            while not VerifyInternetConnection():
                # Reports that there is no internet connection.
                self.PrintWithColor(self.langs['ni'])

            if self.queue != []:
                self.queue_finish.append(self.queue.pop(0))
                data = self.queue_finish[-1]

                PrintCenter("%i/%i" % tuple(self.downloaded))

                for subfolder, URLs in data.items():
                    # The subfolder where the files will be saved is created.
                    subfolder = sep.join(
                        (self.info['folder_out'], ClearName(subfolder)))

                    if len(subfolder) > 220 and not self.ignore_max_length:
                        subfolder = self.__WindowsAdjustRoute(subfolder, 220)

                    makedirs(subfolder, exist_ok=True)

                    # The list of URLs of the files to be saved is iterated.
                    for URL in URLs:
                        if subprocess is not None and subprocess.is_alive():
                            # Wait for the current download to finish.
                            subprocess.join()
                            PrintDivisor()

                        subprocess = Process(
                            target=DownloadFile, daemon=True,
                            args=(
                                URL, subfolder, self.lang,
                                self.continue_downloads,
                                self.ignore_max_length))

                        # It initiates the download
                        subprocess.start()

                self.downloaded[0] += 1

    def SelectLang(self):
        """Language selection screen. It is only called when the language is
        not specified.
        """

        while True:
            _langs = []
            i = 0

            self.PrintWithColor("* Select lang")

            """Prints the languages in numbered form, while storing them in a
            temporary list.
            """
            for key in langs.keys():
                if key == "names_variants": break

                _langs.append(key)
                self.PrintWithColor(
                    f"{i}) {key} ({', '.join(langs['names_variants'][key])})")

                i += 1

            try:
                choice = int(IntputWithColor("Choice: "))
                if choice > (len(_langs)-1): raise ValueError()

                self.lang = _langs[choice]
                self.langs = langs[self.lang]
                self.is_lang_selected = True

                break

            except ValueError:
                PrintDivisor()
                self.PrintWithColor(
                    "ERROR: Invalid option. You must choose one of the "
                    "options shown.")
                PrintDivisor()

    def ObtainPreInfo(self):
        """It asks for the URL, the start page and the number of pages.
        """

        while True:
            if self.URL == "":
                # Print the URL request.
                self.URL = IntputWithColor(
                    self.langs['eU'] + " ").replace(" ", "")

                if not SupportIsAvailable(self.URL):
                    # For incompatible URL.
                    PrintDivisor()
                    self.__NotSupportURLMessages()
                    PrintDivisor()

                    self.URL = ""
                    continue

                elif self.__IsBaseURL(self.URL):
                    # Informs that the URL is incomplete.
                    PrintDivisor()
                    self.URL = ""
                    self.PrintWithColor(self.langs['iu'])
                    continue

            else:
                # Prints the URL passed by arguments.
                self.PrintWithColor(self.langs['u'], self.URL)

            # The URL is checked.
            if not self.URL.lower().startswith("https://") \
                    and not self.URL.lower().startswith("http://"):
                self.URL = "https://" + self.URL

            try:
                response = GetResponse(self.URL, stream=True)
                response.close()

            except (ConnectionError, ReadTimeout) as e:
                PrintDivisor()

                if VerifyInternetConnection():
                    # Informs that there were problems with the URL.
                    self.PrintWithColor(self.langs['iU'])

                else:
                    # Informs that there is an not Internet connection.
                    self.PrintWithColor(self.langs['ni'])
                    raise AppClosed("App closed")

                PrintDivisor()

                self.URL = ""
                continue

            # The start page is requested if it has not been set.
            if self.start is None:
                while True:
                    try:
                        self.start = int(
                            IntputWithColor(self.langs['s'] + " "))
                        break

                    except ValueError:
                        # Informs that the value entered must be an integer.
                        PrintDivisor()
                        self.PrintWithColor(self.langs['tve'])
                        PrintDivisor()

            else:
                # Prints the value given to it.
                self.PrintWithColor(
                    self.langs['info'], self.langs['s'], self.start)

            # The number of pages page is requested if it has not been set.
            if self.pages is None:
                while True:
                    try:
                        self.pages = int(
                            IntputWithColor(self.langs['p'] + " "))

                        if self.pages < 0: self.pages = 0
                        break

                    except ValueError:
                        # Informs that the value entered must be an integer.
                        PrintDivisor()
                        self.PrintWithColor(self.langs['tve'])
                        PrintDivisor()

            else:
                if self.pages < 1:
                    """Prints the word "all" in its respective language when
                    the value of the variable is less than one.
                    """
                    self.PrintWithColor(
                        self.langs['info'], self.langs['p'], self.langs['a'])

                else:
                    # Prints the value given to it.
                    self.PrintWithColor(
                        self.langs['info'], self.langs['p'], self.pages)

                return

            while True:
                """A confirmation is requested to save the data, if not accept
                it, will have to enter all the data again.
                """
                PrintDivisor()
                self.PrintWithColor(self.langs['dyw'])
                option = IntputWithColor(": ")

                if option.upper() == "Y":
                    self.URL = ""
                    self.start = None
                    self.pages = None
                    PrintDivisor()
                    break

                elif option.upper() == "N":
                    return

                else:
                    # Informs that the option is invalid.
                    PrintDivisor()
                    self.PrintWithColor(self.langs['io'])

    def StartObtainingURLs(self):
        """Initiates file getting. This method is always called through a
        thread.
        """

        if self.URL == "" or self.start is None or self.pages is None:
            """Informs that they started to obtain the files without having all
            the data.
            """
            PrintDivisor()
            self.PrintWithColor(self.langs['tlo'])
            return

        temp_start, temp_pages = self.start, self.pages

        while True:
            try:
                """The remaining information and the necessary URLs to
                download the files are obtained.
                """

                for item in GetURLsYield(self.URL, temp_start, temp_pages):
                    if "INFO" in item and item['INFO'] != {}:
                        self.info.update(item['INFO'])

                        self.info['folder_out'] = sep.join((
                            self.info['folder_out'],
                            ClearName(self.info['name'])))

                        if len(self.info['folder_out']) > 200 \
                                and not self.ignore_max_length:

                            self.info['folder_out'] = \
                                self.__WindowsAdjustRoute(
                                    self.info['folder_out'], 200)

                        makedirs(self.info['folder_out'], exist_ok=True)

                        self.info_obtaing = True

                    elif "INFO" in item:
                        # Informs that empty data were received.
                        self.PrintWithColor(self.langs['ed'])
                        return

                    else:
                        if self.info_obtaing:
                            self.queue.append(item)

                        else:
                            """Informs that the necessary information to
                            continue was not obtained.
                            """
                            self.PrintWithColor(self.langs['ti'])
                            return

                break

            except (ConnectionError, ReadTimeout):
                while not VerifyInternetConnection(): pass

                # Organize the variables to continue obtaining the URLs.
                if len(self.queue) != 0 or len(self.queue_finish) != 0:
                    temp_start = \
                        self.start + len(self.queue) + len(self.queue_finish)
                    temp_pages = (self.start + self.pages) - temp_start

            except DeprecationWarning as msg:
                """"msg" is a message from the "getURLs" module that informs
                about code obsolescence.
                """

                # Informs obsolescence.
                self.PrintWithColor(self.langs['tloa'])
                raise AppClosed("App closed")

    def PrintWithColor(self, *text):
        """Method that prints the text with colors.

        It accepts an endless number of arguments which will be converted into
        str for concatenation.
        """

        text = " ".join(str(t) for t in text)
        PrintWithColor(text, self.langs)

    def _FilterArgs(self):
        """Filters the arguments passed to the app.
        """

        try: from .app_help import app_help
        except ImportError: from app_help import app_help

        args = sys.argv[1:]

        if "--help" in args:
            self.PrintWithColor(app_help)
            raise AppClosed("App closed")

        elif "--test" in args:
            self.lang = "English"
            self.langs = langs[self.lang]
            self.is_lang_selected = True
            self.URL = \
                "https://en.novelcool.com/novel/BASTARD-HWANG-YOUNGCHAN.html"
            self.start = 1
            self.pages = 5

            return

        for arg in args:
            if arg.startswith("--lang="):
                value = arg[arg.find("=")+1:]

                if value in langs:
                    self.lang = value
                    self.langs = langs[self.lang]
                    self.is_lang_selected = True

                else:
                    out = []
                    for key in langs.keys():
                        if key == "names_variants": break

                        out.append(
                            f"{key} "
                            f"({', '.join(langs['names_variants'][key])})")

                    self.PrintWithColor(
                        'ARGUMENT ERROR: '
                        f'"{value}" is not a valid language. The '
                        'accepted languages of moments are: '
                        f'{", ".join(out[:-1])} and {out[-1]}.')

                    raise AppClosed("App closed")

            elif arg.startswith("--URL="):
                self.URL = arg[arg.find("=")+1:].replace(" ", "")

                if not SupportIsAvailable(self.URL):
                    self.__NotSupportURLMessages()
                    raise AppClosed("App closed")

                elif self.__IsBaseURL(self.URL):
                    # Informs that the URL is incomplete.
                    self.PrintWithColor(self.langs['iu'])
                    raise AppClosed("App closed")

            elif arg.startswith("--out="):
                self.info['folder_out'] = abspath(
                    arg[arg.find("=")+1:].strip(" "))

                for c in range(32):
                    self.info['folder_out'] = \
                        self.info['folder_out'].replace(chr(c), "")

            elif arg.startswith("--start="):
                try:
                    self.start = int(arg[arg.find("=")+1:])
                    if self.start < 1:
                        self.start = 1

                except ValueError:
                    self.PrintWithColor(
                        "ARGUMENT ERROR: "
                        f'"{arg[arg.find("=")+1:]}" is not a valid value for '
                        '"--start=".')

                    raise AppClosed("App closed")

            elif arg.startswith("--pages="):
                try:
                    self.pages = int(arg[arg.find("=")+1:])
                    if self.pages < 1:
                        self.pages = 0

                except ValueError:
                    self.PrintWithColor(
                        "ARGUMENT ERROR: "
                        f'"{arg[arg.find("=")+1:]}" is not a valid value for'
                        '"--pages=".')

                    raise AppClosed("App closed")

            elif arg.startswith("--continue-downloads"):
                self.continue_downloads = True

            elif arg.startswith("--no-continue-downloads"):
                self.continue_downloads = False

            elif arg.startswith("--ignore-maxlength"):
                self.ignore_max_length = True

            elif arg.startswith("--no-ignore-maxlength"):
                self.ignore_max_length = False

            else:
                self.PrintWithColor(f'ERROR: "{arg}" is an invalid argument.')
                raise AppClosed("App closed")

    def __NotSupportURLMessages(self):
        """It prints an error message indicating that the URL passed as an
        argument is not supported and then prints a list of those that are.
        """

        self.PrintWithColor(self.langs['tUc'] + "\n")
        self.PrintWithColor(self.langs['atm'])

        for key, value in supported.items():
            self.PrintWithColor(key + ":")
            for page in value: self.PrintWithColor("  " + page)

    def __IsBaseURL(self, URL: str):
        """Check if the URL corresponds to the home page of the page.
        """

        URL = URL.strip("/")

        for key, pages in supported.items():
            for page in pages:
                if URL.lower().endswith(page.lower()): return True

        return False

    def __WindowsAdjustRoute(self, route: str, max_length: int):
        """Returns a reduced route. Only works on Windows.
        """

        if sys.platform.startswith("win32"):
            out = AdjustRoute(route, max_length)
            # Notifies the modification of the route.
            self.PrintWithColor(self.langs['td'].format(route, out))

            return out

        else:
            return route
