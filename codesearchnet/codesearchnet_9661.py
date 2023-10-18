def win_set_trans(title, trans, **kwargs):
    """
    Sets the transparency of a window.
    :param title:
    :param trans: A number in the range 0 - 255. The larger the number,
        the more transparent the window will become.
    :param kwargs:
    :return:
    """
    text = kwargs.get("text", "")

    ret = AUTO_IT.AU3_WinSetTrans(LPCWSTR(title), LPCWSTR(text), INT(trans))
    return ret