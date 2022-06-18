"""Code file containing the words and sentences in different languages that
will be printed by the console app, plus some functions.

The text to be printed is loaded from a JSON file named "langs.json".
"""

__all__ = ["FilterLang", "Normalize", "langs"]

from json import JSONDecodeError, dump, load, loads
from os.path import abspath, dirname, sep

langs = {}

def Normalize(text: str) -> str:
    # Substitute stressed vowels and a trisyllable.
    letters = (
        ("áäà", "a"), ("éëè", "e"), ("íïì", "i"), ("óöò", "o"),
        ("úüù", "u"), (("nio",), "ño")
    )

    for let in letters:
        for c in let[0]:
            text = text.replace(c, let[1])
            text = text.replace(c.upper(), let[1].upper())

    return text

def FilterLang(lang: str) -> str:
    # Evaluate if the language is available.
    lang = Normalize(lang).capitalize().strip(" ")

    for language in langs.keys():
        if lang == Normalize(language): return language

    return ""


# Dictionary of sentences.
try:
    if __file__ != "":
        exec_path = dirname(abspath(__file__))
    else:
        import sys
        exec_path = dirname(abspath(sys.argv[0]))

    with open(sep.join((exec_path, "langs.json")), "r", encoding="UTF-8") as f:
        langs = load(f)

    for key, value in langs['names_variants'].items():
        for variant in value: langs[variant] = langs[key]

except (FileNotFoundError, JSONDecodeError) as e:
    try:
        from .app_help import aux_lang
        from .auxfunctions import IntputWithColor, PrintWithColor
    except ImportError:
        from app_help import aux_lang
        from auxfunctions import IntputWithColor, PrintWithColor

    PrintWithColor("ERROR: " + repr(e), {'error': "ERROR"})

    try:
        option = IntputWithColor(
            "ERROR: An error occurred while trying to load the \"langs.json\""
            " file. Please make your choice below:\n1) Replace or overwrite"
            " the content of \"langs.json\" to its state without modifications"
            " (only English and Spanish language will be present).\n2) Do not"
            " continue and close the app.\n3) Continue but do not modify or"
            " create the \"langs.json\" file.\nOption: ", {'error': "ERROR"})

    except KeyboardInterrupt:
        option = "2"

    if option == "1":
        f = open(sep.join((exec_path, "langs.json")), "w", encoding="UTF-8")
        f.write(aux_lang)
        f.close()
        langs = loads(aux_lang)

    elif option == "2":
        import sys
        sys.exit(0)

    elif option == "3":
        langs = loads(aux_lang)

    del aux_lang, f, option

del exec_path
