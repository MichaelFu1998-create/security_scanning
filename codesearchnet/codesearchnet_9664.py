def process_set_priority(process, priority):
    """
    Changes the priority of a process
    :param process: The name or PID of the process to check.
    :param priority:A flag which determines what priority to set
        0 - Idle/Low
        1 - Below Normal (Not supported on Windows 95/98/ME)
        2 - Normal
        3 - Above Normal (Not supported on Windows 95/98/ME)
        4 - High
        5 - Realtime (Use with caution, may make the system unstable)
    :return:
    """
    ret = AUTO_IT.AU3_ProcessSetPriority(LPCWSTR(process), INT(priority))
    if ret == 0:
        if error() == 1:
            raise AutoItError("set priority failed")
        elif error() == 2:
            raise AutoItError("unsupported priority class be used")
    return ret