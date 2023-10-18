def win_activate(title, **kwargs):
    """
    Activates (gives focus to) a window.
    :param title:
    :param text:
    :return:
    """
    text = kwargs.get("text", "")
    ret = AUTO_IT.AU3_WinActivate(LPCWSTR(title), LPCWSTR(text))
    return ret