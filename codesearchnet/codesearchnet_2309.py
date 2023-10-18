def SendUnicodeChar(char: str) -> int:
    """
    Type a single unicode char.
    char: str, len(char) must equal to 1.
    Return int, the number of events that it successfully inserted into the keyboard or mouse input stream.
                If the function returns zero, the input was already blocked by another thread.
    """
    return SendInput(KeyboardInput(0, ord(char), KeyboardEventFlag.KeyUnicode | KeyboardEventFlag.KeyDown),
                     KeyboardInput(0, ord(char), KeyboardEventFlag.KeyUnicode | KeyboardEventFlag.KeyUp))