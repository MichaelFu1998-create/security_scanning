def SendKey(key: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate typing a key.
    key: int, a value in class `Keys`.
    """
    keybd_event(key, 0, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey, 0)
    keybd_event(key, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    time.sleep(waitTime)