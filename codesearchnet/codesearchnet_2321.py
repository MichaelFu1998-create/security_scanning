def EnumAndLogControl(control: Control, maxDepth: int = 0xFFFFFFFF, showAllName: bool = True, startDepth: int = 0) -> None:
    """
    Print and log control and its descendants' propertyies.
    control: `Control` or its subclass.
    maxDepth: int, enum depth.
    showAllName: bool, if False, print the first 30 characters of control.Name.
    startDepth: int, control's current depth.
    """
    for c, d in WalkControl(control, True, maxDepth):
        LogControl(c, d + startDepth, showAllName)