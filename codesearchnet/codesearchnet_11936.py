def partitions(device=""):
    """
    Get a partition list for all disk or for selected device only

    Example::

        from burlap.disk import partitions

        spart = {'Linux': 0x83, 'Swap': 0x82}
        parts = partitions()
        # parts =  {'/dev/sda1': 131, '/dev/sda2': 130, '/dev/sda3': 131}
        r = parts['/dev/sda1'] == spart['Linux']
        r = r and parts['/dev/sda2'] == spart['Swap']
        if r:
            print("You can format these partitions")
    """
    partitions_list = {}
    with settings(hide('running', 'stdout')):
        res = run_as_root('sfdisk -d %(device)s' % locals())

        spart = re.compile(r'(?P<pname>^/.*) : .* Id=(?P<ptypeid>[0-9a-z]+)')
        for line in res.splitlines():
            m = spart.search(line)
            if m:
                partitions_list[m.group('pname')] = int(m.group('ptypeid'), 16)

    return partitions_list