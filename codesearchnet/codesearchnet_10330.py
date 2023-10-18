def get_configuration(filename=CONFIGNAME):
    """Reads and parses the configuration file.

    Default values are loaded and then replaced with the values from
    ``~/.gromacswrapper.cfg`` if that file exists. The global
    configuration instance :data:`gromacswrapper.config.cfg` is updated
    as are a number of global variables such as :data:`configdir`,
    :data:`qscriptdir`, :data:`templatesdir`, :data:`logfilename`, ...

    Normally, the configuration is only loaded when the :mod:`gromacs`
    package is imported but a re-reading of the configuration can be forced
    anytime by calling :func:`get_configuration`.

    :Returns: a dict with all updated global configuration variables
    """
    global cfg, configuration    # very iffy --- most of the whole config mod should a class

    #: :data:`cfg` is the instance of :class:`GMXConfigParser` that makes all
    #: global configuration data accessible
    cfg = GMXConfigParser(filename=filename)   # update module-level cfg
    globals().update(cfg.configuration)        # update configdir, templatesdir ...
    configuration = cfg.configuration          # update module-level configuration
    return cfg