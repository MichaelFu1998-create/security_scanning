def opener(ip_address, port, delay=1):
    """
    Wait a little and then open a web browser page for the control panel.
    """
    global WEBPAGE_OPENED
    if WEBPAGE_OPENED:
        return
    WEBPAGE_OPENED = True
    raw_opener(ip_address, port, delay)