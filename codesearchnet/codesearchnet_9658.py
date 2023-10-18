def win_exists(title, **kwargs):
    """
    Checks to see if a specified window exists.
    :param title: The title of the window to check.
    :param text: The text of the window to check.
    :return: Returns 1 if the window exists, otherwise returns 0.
    """
    text = kwargs.get("text", "")
    ret = AUTO_IT.AU3_WinExists(LPCWSTR(title), LPCWSTR(text))
    return ret