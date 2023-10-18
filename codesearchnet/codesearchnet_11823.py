def address(interface):
    """
    Get the IPv4 address assigned to an interface.

    Example::

        import burlap

        # Print all configured IP addresses
        for interface in burlap.network.interfaces():
            print(burlap.network.address(interface))

    """
    with settings(hide('running', 'stdout')):
        res = (sudo("/sbin/ifconfig %(interface)s | grep 'inet '" % locals()) or '').split('\n')[-1].strip()
    if 'addr' in res:
        return res.split()[1].split(':')[1]
    return res.split()[1]