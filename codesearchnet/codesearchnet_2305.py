def _CreateInput(structure) -> INPUT:
    """
    Create Win32 struct `INPUT` for `SendInput`.
    Return `INPUT`.
    """
    if isinstance(structure, MOUSEINPUT):
        return INPUT(InputType.Mouse, _INPUTUnion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(InputType.Keyboard, _INPUTUnion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(InputType.Hardware, _INPUTUnion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')