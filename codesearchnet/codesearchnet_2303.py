def ReleaseKey(key: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate a key up for key.
    key: int, a value in class `Keys`.
    waitTime: float.
    """
    keybd_event(key, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    time.sleep(waitTime)