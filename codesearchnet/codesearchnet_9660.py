def win_get_state(title, **kwargs):
    """
    Retrieves the state of a given window.
    :param title:
    :param text:
    :return:
    1 = Window exists
    2 = Window is visible
    4 = Windows is enabled
    8 = Window is active
    16 = Window is minimized
    32 = Windows is maximized
    """
    text = kwargs.get("text", "")
    res = AUTO_IT.AU3_WinGetState(LPCWSTR(title), LPCWSTR(text))
    return res