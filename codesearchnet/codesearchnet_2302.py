def PressKey(key: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate a key down for key.
    key: int, a value in class `Keys`.
    waitTime: float.
    """
    keybd_event(key, 0, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey, 0)
    time.sleep(waitTime)