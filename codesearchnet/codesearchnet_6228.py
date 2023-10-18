def interface_to_str(interface):
    """Give a string representation for an optlang interface.

    Parameters
    ----------
    interface : string, ModuleType
        Full name of the interface in optlang or cobra representation.
        For instance 'optlang.glpk_interface' or 'optlang-glpk'.

    Returns
    -------
    string
       The name of the interface as a string
    """
    if isinstance(interface, ModuleType):
        interface = interface.__name__
    return re.sub(r"optlang.|.interface", "", interface)