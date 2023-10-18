def ControlFromHandle(handle: int) -> Control:
    """
    Call IUIAutomation.ElementFromHandle with a native handle.
    handle: int, a native window handle.
    Return `Control` subclass.
    """
    return Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.ElementFromHandle(handle))