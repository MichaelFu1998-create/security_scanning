def process_wait(process, timeout=0):
    """
    Pauses script execution until a given process exists.
    :param process:
    :param timeout:
    :return:
    """
    ret = AUTO_IT.AU3_ProcessWait(LPCWSTR(process), INT(timeout))
    return ret