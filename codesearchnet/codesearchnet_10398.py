def load_v5_tools():
    """ Load Gromacs 2018/2016/5.x tools automatically using some heuristic.

    Tries to load tools (1) using the driver from configured groups (2) and
    falls back to automatic detection from ``GMXBIN`` (3) then to rough guesses.

    In all cases the command ``gmx help`` is ran to get all tools available.

    :return: dict mapping tool names to GromacsCommand classes
    """
    logger.debug("Loading 2018/2016/5.x tools...")

    drivers = config.get_tool_names()

    if len(drivers) == 0 and 'GMXBIN' in os.environ:
        drivers = find_executables(os.environ['GMXBIN'])

    if len(drivers) == 0 or len(drivers) > 4:
        drivers = ['gmx', 'gmx_d', 'gmx_mpi', 'gmx_mpi_d']

    append = config.cfg.getboolean('Gromacs', 'append_suffix', fallback=True)

    tools = {}
    for driver in drivers:
        suffix = driver.partition('_')[2]
        try:
            out = subprocess.check_output([driver, '-quiet', 'help',
                                           'commands'])
            for line in out.splitlines()[5:-1]:
                line = str(line.decode('ascii'))   # Python 3: byte string -> str, Python 2: normal string
                if line[4] != ' ':
                    name = line[4:line.index(' ', 4)]
                    fancy = make_valid_identifier(name)
                    if suffix and append:
                        fancy = '{0!s}_{1!s}'.format(fancy, suffix)
                    tools[fancy] = tool_factory(fancy, name, driver)
        except (subprocess.CalledProcessError, OSError):
            pass

    if not tools:
        errmsg = "Failed to load 2018/2016/5.x tools (tried drivers: {})".format(drivers)
        logger.debug(errmsg)
        raise GromacsToolLoadingError(errmsg)
    logger.debug("Loaded {0} v5 tools successfully!".format(len(tools)))
    return tools