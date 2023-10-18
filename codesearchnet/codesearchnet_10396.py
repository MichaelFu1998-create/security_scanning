def tool_factory(clsname, name, driver, base=GromacsCommand):
    """ Factory for GromacsCommand derived types. """
    clsdict = {
        'command_name': name,
        'driver': driver,
        '__doc__': property(base._get_gmx_docs)
    }
    return type(clsname, (base,), clsdict)