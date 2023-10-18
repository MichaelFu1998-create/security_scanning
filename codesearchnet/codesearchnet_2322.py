def EnumAndLogControlAncestors(control: Control, showAllName: bool = True) -> None:
    """
    Print and log control and its ancestors' propertyies.
    control: `Control` or its subclass.
    showAllName: bool, if False, print the first 30 characters of control.Name.
    """
    lists = []
    while control:
        lists.insert(0, control)
        control = control.GetParentControl()
    for i, control in enumerate(lists):
        LogControl(control, i, showAllName)