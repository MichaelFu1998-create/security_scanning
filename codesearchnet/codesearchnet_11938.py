def ismounted(device):
    """
    Check if partition is mounted

    Example::

        from burlap.disk import ismounted

        if ismounted('/dev/sda1'):
           print ("disk sda1 is mounted")
    """
    # Check filesystem
    with settings(hide('running', 'stdout')):
        res = run_as_root('mount')
    for line in res.splitlines():
        fields = line.split()
        if fields[0] == device:
            return True

    # Check swap
    with settings(hide('running', 'stdout')):
        res = run_as_root('swapon -s')
    for line in res.splitlines():
        fields = line.split()
        if fields[0] == device:
            return True

    return False