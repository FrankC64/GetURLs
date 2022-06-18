import re, shutil, subprocess
from os import listdir, rename, remove
from os.path import abspath, dirname, exists, isdir, sep
from sys import argv, platform

# The main arguments are specified.
if platform.startswith("win32"): PYTHON = "python"
elif platform.startswith("linux"): PYTHON = "python3"
PYTHON_NUITKA = [PYTHON, "-m", "nuitka"]

# Linux dependence: patchelf
try:
    """Checks if the required modules are installed and if any are missing,
    they are installed.
    """

    modules_list = subprocess.run(
        f"{PYTHON} -m pip list", capture_output=True,
        shell=True, check=True, universal_newlines="\n")

    necessary_modules = ["bs4", "cfscrape", "Nuitka"]
    modules = re.findall(r"(?:\n)(.*?)(?: )", modules_list.stdout)

    for module in necessary_modules:
        if module not in modules:
            subprocess.run(
                f"{PYTHON} -m pip install {module}", shell=True, check=True)

except (FileNotFoundError, subprocess.CalledProcessError) as e:
    print("ERROR:", e)
    print("-- Execution Error --")

    exit(1)

# Get the path to this script.
if __file__ != "": build_path = dirname(abspath(__file__))
else: build_path = dirname(abspath(sys.argv[0]))

# Prepare more arguments that will be passed on to Nuitka.
langs_json = f"{sep.join((build_path, 'app', 'langs.json=.'))}"
out_dir = f"{sep.join((build_path, 'Build'))}"
app = f"{sep.join((build_path, 'app', '__main__.py'))}"

nuitka_args = [
    "--standalone", "--follow-imports", "--show-progress",
    "--assume-yes-for-downloads", "--remove-output", f"--output-dir={out_dir}"]

if exists(langs_json[:-2]):
    nuitka_args.append(f"--include-data-file={langs_json}")

# Variable for renaming.
folder_name = f"{sep.join((build_path, 'Build', '__main__.dist'))}"
new_folder_name = f"{sep.join((build_path, 'Build', 'GetURLs'))}"

if platform.startswith("win32"):
    exec_name = \
        f"{sep.join((build_path, 'Build', 'GetURLs', '__main__.exe'))}"
    new_exec_name = \
        f"{sep.join((build_path, 'Build', 'GetURLs', 'GetURLs.exe'))}"
else:
    exec_name = \
        f"{sep.join((build_path, 'Build', 'GetURLs', '__main__'))}"
    new_exec_name = \
        f"{sep.join((build_path, 'Build', 'GetURLs', 'GetURLs'))}"

# An extra argument is added for the specific platform.
if platform.startswith("win32"): nuitka_args.append("--mingw64")

# Construction begins.
try:
    print("-- Start Build --")
    if exists(new_folder_name): shutil.rmtree(new_folder_name)
    if exists(folder_name): shutil.rmtree(folder_name)

    subprocess.run([*PYTHON_NUITKA, *nuitka_args, app], check=True)

    if f"--include-data-file={langs_json}" not in nuitka_args:
        from ca_resource import add_lang_json
        add_lang_json.WriteLangJson(folder_name)

    if platform.startswith("win32"):
        necessary_files = (
            "GetURLs.exe", "_ctypes.pyd", "_multiprocessing.pyd", "_queue.pyd",
            "_socket.pyd", "_ssl.pyd", "certifi", "langs.json",
            "libcrypto-1_1.dll", "libssl-1_1.dll", "select.pyd",
            "unicodedata.pyd", "vcruntime140.dll")

    else:
        necessary_files = (
            "GetURLs", "_blake2.so", "_ctypes.so", "_hashlib.so",
            "_multibytecodec.so", "_multiprocessing.so", "_posixsubprocess.so",
            "_queue.so", "_random.so", "_sha3.so", "_socket.so", "_ssl.so",
            "_struct.so", "array.so", "binascii.so", "certifi", "fcntl.so",
            "langs.json", "math.so", "select.so", "unicodedata.so", "zlib.so")

    # Rename the output folder and the executable.
    if exists(folder_name):
        if not platform.startswith("win32"):
            import shutil

            shutil.move(
                sep.join((folder_name, "certifi")),
                sep.join((out_dir, "certifi")))

            rename(folder_name, new_folder_name)

            shutil.move(
                sep.join((out_dir, "certifi")),
                sep.join((new_folder_name, "certifi")))

        else:
            rename(folder_name, new_folder_name)

        print("INFO:", folder_name, "renamed to", new_folder_name)

        rename(exec_name, new_exec_name)
        print("INFO:", exec_name, "renamed to", new_exec_name)

    # Starts the deletion of unnecessary files.
    for element in listdir(new_folder_name):
        if not (element.startswith("python") and element.endswith(".dll")) \
                and element not in necessary_files:

            if isdir(sep.join((new_folder_name, element))):
                shutil.rmtree(sep.join((new_folder_name, element)))
            else:
                remove(sep.join((new_folder_name, element)))

            print(sep.join((new_folder_name, element)), "(removed)")

    print("-- Successful Build --")

except (FileNotFoundError, subprocess.CalledProcessError) as e:
    print("ERROR:", e)
    print("-- Execution Error --")
