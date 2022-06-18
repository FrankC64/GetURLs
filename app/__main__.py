try:
    from . import (
        AppClosed, ConsoleApp, PrintDivisor, PrintWithColor, auxfunctions)

except ImportError:
    import auxfunctions
    AppClosed = __import__("__init__").AppClosed
    ConsoleApp = __import__("__init__").ConsoleApp
    PrintDivisor = __import__("__init__").PrintDivisor
    PrintWithColor = __import__("__init__").PrintWithColor

def main():
    """Main method that calls the app class.
    """

    try:
        ConsoleApp().Start()

    except (EOFError, KeyboardInterrupt):
        pass

    except AppClosed:
        pass

    except FileNotFoundError:
        PrintWithColor(
            "An attempt was made to create a folder and the operation "
            "failed. If you are on Windows try moving the script or "
            "executable to a different folder.")

    except Exception as e:
        PrintDivisor()
        PrintWithColor(
            "ERROR: An unexpected and uncontrolled error occurred.",
            {"error": "ERROR:"})

        PrintWithColor("ERROR: " + repr(e), {"error": "ERROR:"})

    PrintWithColor("\n\nApp closed.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        # Recapture KeyboardInterrupt due to problems with nuitka.
        pass

    auxfunctions.DefaultColor()

    # https://es.novelcool.com/novel/BASTARD-HWANG-YOUNGCHAN.html
