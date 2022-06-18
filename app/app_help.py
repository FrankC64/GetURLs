"""It contains the help text of the application and also contains the messages
in different languages in case the "langs.json" file is missing or cannot be
read.
"""

app_help = """
--help
    Displays the arguments accepted by the app and information about them.

* PRE-INFORMATION:
--URL=
    URL to be used by the app to obtain the files.

--start=
    Page from where the obtaining will be started. Accepts only positive
    integers.

    NOTE: This value can be modified if the start page exceeds the current one,
    so the last page will be set as the start page.

--pages=
    Number of pages from the start page to get the files. Only integers are
    accepted. If you specify a value less than one, it will be interpreted
    that you want to get the files of all pages from the start page.

    NOTE: This value can be modified if the number of pages requested is
    greater than the number of pages available since the start page, so the
    value will be set to the number of pages available.

--lang=
    Argument to choose the language and skip this step within the app.
    Variants of the same language in other languages used by the app are
    accepted.

--out=
    File output path. If a path is not specified, you choose the path where the
    app was called and create a subfolder called "Downloads".

* FLAGS:
--continue-downloads
    This flag is used to continue downloads that have not been completed. It is
    enabled by default.

--no-continue-downloads
    This flag is used to not continue downloads that have not been completed.
    When the program is run with this flag files with names equal to the files
    to be downloaded are deleted, no matter if the files are partially or fully
    downloaded.

* FLAGS FOR WINDOWS:
--ignore-maxlength
    Windows-only flag to limit the number of characters in the file path. It
    is set as a limit of 240 characters and the app will not continue if the
    output path exceeds 180 characters, this applies only when an output path
    is specified and for the download path given by the app when one is not
    specified.

    The path limitation works as follows: the output path plus the folder with
    the name of the series to download has a limit of 200 characters, the
    aforementioned path plus the folder with the name of the chapter/subtitle
    has a limit of 220 characters and the full path plus the name of the file
    to download has a limit of 240 characters.

--no-ignore-maxlength
    It does not reduce the length of download paths.
"""

aux_lang = """{
    "English": {
        "ls": "INFO: Language selected:",
        "eU": "Enter the URL:",
        "iU": "ERROR: An error occurred while validating the URL. Please try again or enter another URL.",
        "info": "INFO:",
        "error": "ERROR:",
        "s": "Start:",
        "p": "Pages:",
        "tUc": "ERROR: The URL currently entered is not supported.",
        "atm": "INFO: At the moment only the following pages are supported:",
        "tve": "INFO: The value entered must be a whole number.",
        "dyw": "Do you want to re-enter the data? (Y) to return or (N) to continue.",
        "a": "all",
        "io": "ERROR: Invalid option.",
        "tlo": "ERROR: The URLs obtaining has been started without having all the data.",
        "tloa": "ERROR: The URL obtaining algorithm is obsolete for the requested page, so it is impossible to continue obtaining URLs.",
        "oin": "INFO: Obtaining information...",
        "sn": "INFO: Series name: {0}",
        "f": "INFO: Folder path: {0}",
        "st": "INFO: Start: {0} > {1}",
        "pa": "INFO: Pages: {0} > {1}",
        "ed": "ERROR: Empty data was received.",
        "d": "INFO: Downloading \\"{0}\\"...",
        "ni": "ERROR: No internet connection.",
        "tf": "INFO: The file \\"{0}\\" was already downloaded.",
        "si": "Size:",
        "sp": "Speed:",
        "hb": "INFO: \\"{0}\\" has been downloaded.",
        "au": "ERROR: An unexpected and uncontrolled error occurred.",
        "tfao": "ERROR: The folder and/or file path have been deleted, so the download will restart from the beginning.",
        "tpe": "The path \\"{0}\\" exceeds the 180 character limit. Choose a shorter path for download output or disable the character limit with the \\"--ignore-maxlength\\" flag.",
        "ti": "ERROR: The information required to continue has not been obtained correctly for unknown reasons.",
        "u": "INFO: URL:",
        "iu": "ERROR: Incomplete URL. Base URLs or home pages are not accepted, pass a URL with a specific destination.",
        "td": "INFO: The path \\"{0}\\" has been reduced and converted to \\"{1}\\"."
        },

    "Español": {
        "ls": "INFO: Idioma seleccionado:",
        "eU": "Introduzca la URL:",
        "iU": "ERROR: Se ha producido un error al validar la URL. Por favor, inténtelo de nuevo o introduzca otra URL.",
        "info": "INFO:",
        "error": "ERROR:",
        "s": "Inicio:",
        "p": "Páginas:",
        "tUc": "ERROR: La URL introducida actualmente no es compatible.",
        "atm": "INFO: Por el momento sólo se admiten las siguientes páginas:",
        "tve": "INFO: El valor introducido debe ser un número entero.",
        "dyw": "¿Deseas volver a introducir los datos? (Y) para volver o (N) para continuar.",
        "a": "todas",
        "io": "ERROR: Opción inválida.",
        "tlo": "ERROR: La obtención de los URLs se ha iniciado sin tener todos los datos.",
        "tloa": "ERROR: El algoritmo de obtención de URLs es obsoleto para la página solicitada, por lo que es imposible continuar la obtención.",
        "oin": "INFO: Obteniendo información...",
        "sn": "INFO: Nombre de la serie: {0}",
        "f": "INFO: Ruta de la carpeta: {0}",
        "st": "INFO: Inicio: {0} > {1}",
        "pa": "INFO: Páginas: {0} > {1}",
        "ed": "ERROR: Se han recibido datos vacíos.",
        "d": "INFO: Descargando \\"{0}\\"...",
        "ni": "ERROR: No hay conexión a internet.",
        "tf": "INFO: El archivo \\"{0}\\" ya estaba descargado.",
        "si": "Tamaño:",
        "sp": "Velocidad:",
        "hb": "INFO: \\"{0}\\" ha sido descargado.",
        "au": "ERROR: Se produjo un error no esperado ni controlado.",
        "tfao": "ERROR: La carpeta y/o la ruta del archivo han sido eliminados, por lo que la descarga se reiniciará desde el principio.",
        "tpe": "La ruta \\"{0}\\" excede el limite de 180 caracteres. Elija una ruta más corta para la salida de las descargas o inhabilite el límite de caracteres con la bandera \\"--ignore-maxlength\\".",
        "ti": "ERROR: La información necesaria para continuar no se ha obtenido correctamente por razones desconocidas.",
        "u": "INFO: URL:",
        "iu": "ERROR: URL incompleta. No se aceptan URLs base o páginas de inicio, pase una URL con un destino específico.",
        "td": "INFO: La ruta \\"{0}\\" ha sido reducida y convertida en \\"{1}\\"."
        },

    "names_variants": {
        "English": ["Inglés"],
        "Español": ["Spanish"]
    }
}
"""
