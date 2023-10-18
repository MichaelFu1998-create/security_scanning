def ResetConsoleColor() -> bool:
    """
    Reset to the default text color on console window.
    Return bool, True if succeed otherwise False.
    """
    if sys.stdout:
        sys.stdout.flush()
    bool(ctypes.windll.kernel32.SetConsoleTextAttribute(_ConsoleOutputHandle, _DefaultConsoleColor))