def RunScriptAsAdmin(argv: list, workingDirectory: str = None, showFlag: int = SW.ShowNormal) -> bool:
    """
    Run a python script as administrator.
    System will show a popup dialog askes you whether to elevate as administrator if UAC is enabled.
    argv: list, a str list like sys.argv, argv[0] is the script file, argv[1:] are other arguments.
    workingDirectory: str, the working directory for the script file.
    showFlag: int, a value in class `SW`.
    Return bool, True if succeed.
    """
    args = ' '.join('"{}"'.format(arg) for arg in argv)
    return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, workingDirectory, showFlag) > 32