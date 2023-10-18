def ControlFromPoint(x: int, y: int) -> Control:
    """
    Call IUIAutomation ElementFromPoint x,y. May return None if mouse is over cmd's title bar icon.
    Return `Control` subclass or None.
    """
    element = _AutomationClient.instance().IUIAutomation.ElementFromPoint(ctypes.wintypes.POINT(x, y))
    return Control.CreateControlFromElement(element)