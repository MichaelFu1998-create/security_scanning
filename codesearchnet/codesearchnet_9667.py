def run_as(user, domain, password, filename, logon_flag=1, work_dir="",
           show_flag=Properties.SW_SHOWNORMAL):
    """
    Runs an external program.
    :param user: username The user name to use.
    :param domain: The domain name to use.
    :param password: The password to use.
    :param logon_flag: 0 = do not load the user profile, 1 = (default) load
        the user profile, 2 = use for net credentials only
    :param filename: The name of the executable (EXE, BAT, COM, or PIF) to run.
    :param work_dir: The working directory.
    :param show_flag: The "show" flag of the executed program:
        SW_HIDE = Hidden window
        SW_MINIMIZE = Minimized window
        SW_MAXIMIZE = Maximized window
    :return:
    """
    ret = AUTO_IT.AU3_RunAs(
        LPCWSTR(user), LPCWSTR(domain), LPCWSTR(password), INT(logon_flag),
        LPCWSTR(filename), LPCWSTR(work_dir), INT(show_flag)
    )
    return ret