def _list_networks():
    """Return a dictionary of network name to active status bools.

        Sample virsh net-list output::

    Name                 State      Autostart
    -----------------------------------------
    default              active     yes
    juju-test            inactive   no
    foobar               inactive   no

    Parsing the above would return::
    {"default": True, "juju-test": False, "foobar": False}

    See: http://goo.gl/kXwfC
    """
    output = core.run("virsh net-list --all")
    networks = {}

    # Take the header off and normalize whitespace.
    net_lines = [n.strip() for n in output.splitlines()[2:]]
    for line in net_lines:
        if not line:
            continue
        name, state, auto = line.split()
        networks[name] = state == "active"
    return networks