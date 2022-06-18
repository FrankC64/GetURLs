import os, re, subprocess, sys

BIN = "/bin"
PATTERN = r"(?:\n)(.*?term.*?)(?:\n)"
TERMINALS = ("konsole", "roxterm", "lxterminal", "gnome-terminal", "xterm")

terminals = "\n" + "\n\n".join(os.listdir(BIN)) + "\n"
terminals = re.findall(PATTERN, terminals)

for terminal in terminals:
    if terminal.lower() in TERMINALS:
        subprocess.run(
            f'{terminal} -e "python -m app {" ".join(sys.argv[1:])}; bash"',
            capture_output=True, check=True,
            shell=True)
        break

else:
    print("ERROR: No terminal was found.")
