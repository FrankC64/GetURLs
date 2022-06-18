# Get URLs (Console-App)
This is a console application that takes advantage of the benefits of the GetURLs module, so that it can be used without the need for code.

## Run the program (not compile)
The program can be executed in the following ways:

1- From **Sublime Text** (open project): **Tools -> Build System -> Main**. This way always opens an external window for the execution of the program.
2- From the terminal, being in the root of the project, type "**python -m app**" in Windows and "**python3 -m app**" in Linux. You can also directly execute **\__main__.py**.

## Compile the program
To compile the program there are two ways to do it. The first one is through Sublime Text, when the project is opened in Tools -> Build System, two options will be added, to compile the program choose the "Build" option. The second way is by directly executing the "build.py" file located in the root of the project.

The project build will be located in "./Build/GetURLs".

## Sublime Text Builds
* **Main:** Runs the program.
* **Main (test):** Runs the program with predefined information.
* **Build:** Builds the program.
* **Add langs.json:** Adds the langs.json file to the app folder.

## Dependencies
**Python:**
```
BeautifulSoup (python3 -m pip install bs4)
cfscrape (python3 -m pip install cfscrape)
nuitka (python3 -m pip install nuitka)
```

**NOTA:** When trying to compile the program, if any of the three modules mentioned above is not found, it will be installed automatically.

**For Linux:**
```
patchelf (sudo apt-get install patchelf)
build-essential (sudo apt-get install build-essential)
```

**For Windows:**
For Windows you must download a MinGW compiler, it can be found at [WinLibs](https://winlibs.com/).

## Documentation
See the documentation in the "documentation.txt" file.
