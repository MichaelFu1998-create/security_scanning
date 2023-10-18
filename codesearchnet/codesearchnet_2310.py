def _VKtoSC(key: int) -> int:
    """
    This function is only for internal use in SendKeys.
    key: int, a value in class `Keys`.
    Return int.
    """
    if key in _SCKeys:
        return _SCKeys[key]
    scanCode = ctypes.windll.user32.MapVirtualKeyA(key, 0)
    if not scanCode:
        return 0
    keyList = [Keys.VK_APPS, Keys.VK_CANCEL, Keys.VK_SNAPSHOT, Keys.VK_DIVIDE, Keys.VK_NUMLOCK]
    if key in keyList:
        scanCode |= 0x0100
    return scanCode