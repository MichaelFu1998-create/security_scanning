def create_connection(port=_PORT_, timeout=_TIMEOUT_, restart=False):
    """
    Create Bloomberg connection

    Returns:
        (Bloomberg connection, if connection is new)
    """
    if _CON_SYM_ in globals():
        if not isinstance(globals()[_CON_SYM_], pdblp.BCon):
            del globals()[_CON_SYM_]

    if (_CON_SYM_ in globals()) and (not restart):
        con = globals()[_CON_SYM_]
        if getattr(con, '_session').start(): con.start()
        return con, False

    else:
        con = pdblp.BCon(port=port, timeout=timeout)
        globals()[_CON_SYM_] = con
        con.start()
        return con, True