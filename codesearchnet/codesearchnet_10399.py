def load_v4_tools():
    """ Load Gromacs 4.x tools automatically using some heuristic.

    Tries to load tools (1) in configured tool groups (2) and fails back  to
    automatic detection from ``GMXBIN`` (3) then to a prefilled list.

    Also load any extra tool configured in ``~/.gromacswrapper.cfg``

    :return: dict mapping tool names to GromacsCommand classes
    """
    logger.debug("Loading v4 tools...")

    names = config.get_tool_names()

    if len(names) == 0 and 'GMXBIN' in os.environ:
        names = find_executables(os.environ['GMXBIN'])

    if len(names) == 0 or len(names) > len(V4TOOLS) * 4:
        names = list(V4TOOLS)

    names.extend(config.get_extra_tool_names())

    tools = {}
    for name in names:
        fancy = make_valid_identifier(name)
        tools[fancy] = tool_factory(fancy, name, None)

    if not tools:
        errmsg = "Failed to load v4 tools"
        logger.debug(errmsg)
        raise GromacsToolLoadingError(errmsg)
    logger.debug("Loaded {0} v4 tools successfully!".format(len(tools)))
    return tools