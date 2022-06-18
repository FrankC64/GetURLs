"""Extension of "auxfunctions" to be able to print with colors in Windows.

Why don't I include the code from this file in auxfunctions?
Because for Windows I need to make several calls to its API, in addition to
prepare functions and variables, which does not follow the full Python code
structure of auxfunctions.
"""
__all__ = ["PrintWithColor", "IntputWithColor", "DefaultColor"]

import ctypes.wintypes
import sys

LIBC = ctypes.cdll.msvcrt
KERNEL32 = ctypes.windll.kernel32
STDOUT_HANDLE = None
DEFAULT_COLOR = None

SetConsoleTextAttribute = KERNEL32.SetConsoleTextAttribute
SetConsoleTextAttribute.argtypes = (
    ctypes.wintypes.HANDLE, ctypes.wintypes.WORD)
SetConsoleTextAttribute.restype = ctypes.c_bool

wprintf = LIBC.wprintf

def __PreparedConstants():
    """This function is called when the code is imported and prepares the
    constants to be used in the code.
    """

    global STDOUT_HANDLE, DEFAULT_COLOR

    class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.wintypes._COORD),
            ("dwCursorPosition", ctypes.wintypes._COORD),
            ("wAttributes", ctypes.wintypes.WORD),
            ("srWindow", ctypes.wintypes._SMALL_RECT),
            ("dwMaximumWindowSize", ctypes.wintypes._COORD)
        ]

    GetStdHandle = KERNEL32.GetStdHandle
    GetStdHandle.argtypes = (ctypes.wintypes.DWORD,)
    GetStdHandle.restype = ctypes.wintypes.HANDLE

    GetConsoleScreenBufferInfo = KERNEL32.GetConsoleScreenBufferInfo
    GetConsoleScreenBufferInfo.argtypes = (
        ctypes.wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO))
    GetConsoleScreenBufferInfo.restype = ctypes.c_bool

    # Set constants.
    STDOUT_HANDLE = GetStdHandle(-11)
    DEFAULT_COLOR = CONSOLE_SCREEN_BUFFER_INFO()

    if GetConsoleScreenBufferInfo(STDOUT_HANDLE, ctypes.byref(DEFAULT_COLOR)):
        DEFAULT_COLOR = DEFAULT_COLOR.wAttributes
    else:
        DEFAULT_COLOR = 7

def PrintWithColor(
        text: str, langs: dict = {}, color: str = "", end: str = "\n"):
    """Prints the string passed as the first argument with the color
    corresponding to the information found in langs or in default with the
    specified color.
    """

    if ('info' in langs) and text.startswith(langs['info']):
        SetConsoleTextAttribute(STDOUT_HANDLE, 6)
        wprintf(langs['info'])
        SetConsoleTextAttribute(STDOUT_HANDLE, 7)
        wprintf(text[len(langs['info']):] + end)

    elif text.startswith("ARGUMENT ERROR:"):
        SetConsoleTextAttribute(STDOUT_HANDLE, 4)
        wprintf("ARGUMENT ERROR:")
        SetConsoleTextAttribute(STDOUT_HANDLE, 7)
        wprintf(text[len("ARGUMENT ERROR:"):] + end)

    elif ('error' in langs) and text.startswith(langs['error']):
        SetConsoleTextAttribute(STDOUT_HANDLE, 4)
        wprintf(langs['error'])
        SetConsoleTextAttribute(STDOUT_HANDLE, 7)
        wprintf(text[len(langs['error']):] + end)

    elif ('si' in langs) and text.startswith(langs['si']):
        SetConsoleTextAttribute(STDOUT_HANDLE, 2)
        wprintf(langs['si'])
        SetConsoleTextAttribute(STDOUT_HANDLE, 7)
        wprintf(text[len(langs['si']):text.find(langs['sp'])])
        SetConsoleTextAttribute(STDOUT_HANDLE, 2)
        wprintf(langs['sp'])
        SetConsoleTextAttribute(STDOUT_HANDLE, 7)
        wprintf(text[text.find(langs['sp'])+len(langs['sp']):] + end)

    else:
        if color == "BLUE":
            SetConsoleTextAttribute(STDOUT_HANDLE, 1)
            wprintf(text + end)
            SetConsoleTextAttribute(STDOUT_HANDLE, 7)

        else:
            SetConsoleTextAttribute(STDOUT_HANDLE, 7)
            wprintf(text + end)

def IntputWithColor(text: str, langs: dict = {}, color: str = ""):
    """It prints the passed text with color just like "PrintWithColor" and then
    it is put in standby to accept keyboard input like the "input" function.
    """

    PrintWithColor(text, langs, color, "")
    return input()

def DefaultColor():
    """Sets the terminal colors to their default state.
    """

    SetConsoleTextAttribute(STDOUT_HANDLE, DEFAULT_COLOR)


__PreparedConstants()
# UTF-8 for wprintf.
LIBC._setmode(sys.stdout.fileno(), 0x40000)
