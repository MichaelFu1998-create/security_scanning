def interfaces():
    """
    Get the list of network interfaces. Will return all datalinks on SmartOS.
    """
    with settings(hide('running', 'stdout')):
        if is_file('/usr/sbin/dladm'):
            res = run('/usr/sbin/dladm show-link')
        else:
            res = sudo('/sbin/ifconfig -s')
    return [line.split(' ')[0] for line in res.splitlines()[1:]]