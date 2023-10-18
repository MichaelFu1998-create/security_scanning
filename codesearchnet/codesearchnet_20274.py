def get_plugin_source(module=None, stacklevel=None):
    """Returns the :class:`PluginSource` for the current module or the given
    module.  The module can be provided by name (in which case an import
    will be attempted) or as a module object.

    If no plugin source can be discovered, the return value from this method
    is `None`.

    This function can be very useful if additional data has been attached
    to the plugin source.  For instance this could allow plugins to get
    access to a back reference to the application that created them.

    :param module: optionally the module to locate the plugin source of.
    :param stacklevel: defines how many levels up the module should search
                       for before it discovers the plugin frame.  The
                       default is 0.  This can be useful for writing wrappers
                       around this function.
    """
    if module is None:
        frm = sys._getframe((stacklevel or 0) + 1)
        name = frm.f_globals['__name__']
        glob = frm.f_globals
    elif isinstance(module, string_types):
        frm = sys._getframe(1)
        name = module
        glob = __import__(module, frm.f_globals,
                          frm.f_locals, ['__dict__']).__dict__
    else:
        name = module.__name__
        glob = module.__dict__
    return _discover_space(name, glob)