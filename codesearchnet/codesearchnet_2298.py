def PlayWaveFile(filePath: str = r'C:\Windows\Media\notify.wav', isAsync: bool = False, isLoop: bool = False) -> bool:
    """
    Call PlaySound from Win32.
    filePath: str, if emtpy, stop playing the current sound.
    isAsync: bool, if True, the sound is played asynchronously and returns immediately.
    isLoop: bool, if True, the sound plays repeatedly until PlayWaveFile(None) is called again, must also set isAsync to True.
    Return bool, True if succeed otherwise False.
    """
    if filePath:
        SND_ASYNC = 0x0001
        SND_NODEFAULT = 0x0002
        SND_LOOP = 0x0008
        SND_FILENAME = 0x20000
        flags = SND_NODEFAULT | SND_FILENAME
        if isAsync:
            flags |= SND_ASYNC
        if isLoop:
            flags |= SND_LOOP
            flags |= SND_ASYNC
        return bool(ctypes.windll.winmm.PlaySoundW(ctypes.c_wchar_p(filePath), ctypes.c_void_p(0), flags))
    else:
        return bool(ctypes.windll.winmm.PlaySoundW(ctypes.c_wchar_p(0), ctypes.c_void_p(0), 0))