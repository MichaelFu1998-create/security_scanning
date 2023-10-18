def process_wait_close(process, timeout=0):
    """
    Pauses script execution until a given process does not exist.
    :param process:
    :param timeout:
    :return:
    """
    ret = AUTO_IT.AU3_ProcessWaitClose(LPCWSTR(process), INT(timeout))
    return ret