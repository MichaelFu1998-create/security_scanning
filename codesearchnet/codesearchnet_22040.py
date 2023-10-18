def githubtunnel(user1, server1, user2, server2, port, verbose, stanford=False):
    """
    Opens a nested tunnel, first to *user1*@*server1*, then to *user2*@*server2*, for accessing on *port*.

    If *verbose* is true, prints various ssh commands.

    If *stanford* is true, shifts ports up by 1.

    Attempts to get *user1*, *user2* from environment variable ``USER_NAME`` if called from the command line.
    """
    if stanford:
        port_shift = 1
    else:
        port_shift = 0

    # command1 = 'ssh -nNf -L {}:quickpicmac3.slac.stanford.edu:22 {}@{}'.format(port, user, server)
    command1 = 'ssh -nNf -L {}:{}:22 {}@{}'.format(port-1-port_shift, server2, user1, server1)
    command2 = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -nNf -L {}:cardinal.stanford.edu:22 -p {} {}@localhost'.format(port-port_shift, port-port_shift-1, user2)
    command3 = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -nNf -L {}:github.com:22 -p {} {}@localhost'.format(port, port-1, user2)
    if verbose:
        print(command1)
        if stanford:
            print(command2)
        print(command3)
    try:
        call(shlex.split(command1))
        if stanford:
            call(shlex.split(command2))
        call(shlex.split(command3))
    except:
        print('Failure!')
        pass