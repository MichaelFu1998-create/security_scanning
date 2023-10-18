def IsDesktopLocked() -> bool:
    """
    Check if desktop is locked.
    Return bool.
    Desktop is locked if press Win+L, Ctrl+Alt+Del or in remote desktop mode.
    """
    isLocked = False
    desk = ctypes.windll.user32.OpenDesktopW(ctypes.c_wchar_p('Default'), 0, 0, 0x0100)  # DESKTOP_SWITCHDESKTOP = 0x0100
    if desk:
        isLocked = not ctypes.windll.user32.SwitchDesktop(desk)
        ctypes.windll.user32.CloseDesktop(desk)
    return isLocked