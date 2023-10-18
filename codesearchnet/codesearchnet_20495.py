def rcfile(appname, section=None, args={}, strip_dashes=True):
    """Read environment variables and config files and return them merged with
    predefined list of arguments.

    Parameters
    ----------
    appname: str
        Application name, used for config files and environment variable
        names.

    section: str
        Name of the section to be read. If this is not set: appname.

    args:
        arguments from command line (optparse, docopt, etc).

    strip_dashes: bool
        Strip dashes prefixing key names from args dict.

    Returns
    --------
    dict
        containing the merged variables of environment variables, config
        files and args.

    Raises
    ------
    IOError
        In case the return value is empty.

    Notes
    -----
    Environment variables are read if they start with appname in uppercase
    with underscore, for example:

        TEST_VAR=1

    Config files compatible with ConfigParser are read and the section name
    appname is read, example:

        [appname]
        var=1

    We can also have host-dependent configuration values, which have
    priority over the default appname values.

        [appname]
        var=1

        [appname:mylinux]
        var=3


    For boolean flags do not try to use: 'True' or 'False',
                                         'on' or 'off',
                                         '1' or '0'.
    Unless you are willing to parse this values by yourself.
    We recommend commenting the variables out with '#' if you want to set a
    flag to False and check if it is in the rcfile cfg dict, i.e.:

        flag_value = 'flag_variable' in cfg


    Files are read from: /etc/appname/config,
                         /etc/appfilerc,
                         ~/.config/appname/config,
                         ~/.config/appname,
                         ~/.appname/config,
                         ~/.appnamerc,
                         appnamerc,
                         .appnamerc,
                         appnamerc file found in 'path' folder variable in args,
                         .appnamerc file found in 'path' folder variable in args,
                         file provided by 'config' variable in args.

    Example
    -------
        args = rcfile(__name__, docopt(__doc__, version=__version__))
    """
    if strip_dashes:
        for k in args.keys():
            args[k.lstrip('-')] = args.pop(k)

    environ = get_environment(appname)

    if section is None:
        section = appname

    config = get_config(appname,
                        section,
                        args.get('config', ''),
                        args.get('path', ''))
    config = merge(merge(args, config), environ)

    if not config:
        raise IOError('Could not find any rcfile for application '
                      '{}.'.format(appname))

    return config