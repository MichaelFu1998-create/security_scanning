def ControlsAreSame(control1: Control, control2: Control) -> bool:
    """
    control1: `Control` or its subclass.
    control2: `Control` or its subclass.
    Return bool, True if control1 and control2 represent the same control otherwise False.
    """
    return bool(_AutomationClient.instance().IUIAutomation.CompareElements(control1.Element, control2.Element))