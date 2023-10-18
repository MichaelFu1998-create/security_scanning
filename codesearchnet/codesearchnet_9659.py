def win_get_caret_pos():
    """
    Returns the coordinates of the caret in the foreground window
    :return:
    """
    p = POINT()
    AUTO_IT.AU3_WinGetCaretPos(byref(p))
    return p.x, p.y