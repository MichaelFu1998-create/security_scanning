def ControlFromPoint2(x: int, y: int) -> Control:
    """
    Get a native handle from point x,y and call IUIAutomation.ElementFromHandle.
    Return `Control` subclass.
    """
    return Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.ElementFromHandle(WindowFromPoint(x, y)))