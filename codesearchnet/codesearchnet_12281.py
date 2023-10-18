def get_lcformat(formatkey, use_lcformat_dir=None):
    '''This loads an LC format description from a previously-saved JSON file.

    Parameters
    ----------

    formatkey : str
        The key used to refer to the LC format. This is part of the JSON file's
        name, e.g. the format key 'hat-csv' maps to the format JSON file:
        '<astrobase install path>/data/lcformats/hat-csv.json'.

    use_lcformat_dir : str or None
        If provided, must be the path to a directory that contains the
        corresponding lcformat JSON file for `formatkey`. If this is None, this
        function will look for lcformat JSON files corresponding to the given
        `formatkey`:

        - first, in the directory specified in this kwarg,
        - if not found there, in the home directory: ~/.astrobase/lcformat-jsons
        - if not found there, in: <astrobase install path>/data/lcformats

    Returns
    -------

    tuple
        A tuple of the following form is returned::

            (fileglob       : the file glob of the associated LC files,
             readerfunc_in  : the imported Python function for reading LCs,
             timecols       : list of time col keys to get from the lcdict,
             magcols        : list of mag col keys to get from the lcdict ,
             errcols        : list of err col keys to get from the lcdict,
             magsarefluxes  : True if the measurements are fluxes not mags,
             normfunc_in    : the imported Python function for normalizing LCs)

        All `astrobase.lcproc` functions can then use this tuple to dynamically
        import your LC reader and normalization functions to work with your LC
        format transparently.

    '''

    if isinstance(use_lcformat_dir, str):

        # look for the lcformat JSON
        lcformat_jsonpath = os.path.join(
            use_lcformat_dir,
            '%s.json' % formatkey
        )

        if not os.path.exists(lcformat_jsonpath):

            lcformat_jsonpath = os.path.join(
                os.path.expanduser('~/.astrobase/lcformat-jsons'),
                '%s.json' % formatkey
            )

            if not os.path.exists(lcformat_jsonpath):

                install_path = os.path.dirname(__file__)
                install_path = os.path.abspath(
                    os.path.join(install_path, '..', 'data','lcformats')
                )

                lcformat_jsonpath = os.path.join(
                    install_path,
                    '%s.json' % formatkey
                )

                if not os.path.exists(lcformat_jsonpath):
                    LOGERROR('could not find an lcformat JSON '
                             'for formatkey: %s in any of: '
                             'use_lcformat_dir, home directory, '
                             'astrobase installed data directory'
                             % formatkey)
                    return None

    else:

        lcformat_jsonpath = os.path.join(
            os.path.expanduser('~/.astrobase/lcformat-jsons'),
            '%s.json' % formatkey
        )

        if not os.path.exists(lcformat_jsonpath):

            install_path = os.path.dirname(__file__)
            install_path = os.path.abspath(
                os.path.join(install_path, '..', 'data','lcformats')
            )

            lcformat_jsonpath = os.path.join(
                install_path,
                '%s.json' % formatkey
            )

            if not os.path.exists(lcformat_jsonpath):
                LOGERROR('could not find an lcformat JSON '
                         'for formatkey: %s in any of: '
                         'use_lcformat_dir, home directory, '
                         'astrobase installed data directory'
                         % formatkey)
                return None

    # load the found lcformat JSON
    with open(lcformat_jsonpath) as infd:
        lcformatdict = json.load(infd)

    readerfunc_module = lcformatdict['lcreader_module']
    readerfunc = lcformatdict['lcreader_func']
    readerfunc_kwargs = lcformatdict['lcreader_kwargs']
    normfunc_module = lcformatdict['lcnorm_module']
    normfunc = lcformatdict['lcnorm_func']
    normfunc_kwargs = lcformatdict['lcnorm_kwargs']

    fileglob = lcformatdict['fileglob']
    timecols = lcformatdict['timecols']
    magcols = lcformatdict['magcols']
    errcols = lcformatdict['errcols']
    magsarefluxes = lcformatdict['magsarefluxes']

    # import all the required bits
    # see if we can import the reader module
    readermodule = _check_extmodule(readerfunc_module, formatkey)

    if not readermodule:
        LOGERROR("could not import the required "
                 "module: %s to read %s light curves" %
                 (readerfunc_module, formatkey))
        return None

    # then, get the function we need to read the light curve
    try:
        readerfunc_in = getattr(readermodule, readerfunc)
    except AttributeError:
        LOGEXCEPTION('Could not get the specified reader '
                     'function: %s for lcformat: %s '
                     'from module: %s'
                     % (formatkey, readerfunc_module, readerfunc))
        raise

    # see if we can import the normalization module
    if normfunc_module:
        normmodule = _check_extmodule(normfunc_module, formatkey)
        if not normmodule:
            LOGERROR("could not import the required "
                     "module: %s to normalize %s light curves" %
                     (normfunc_module, formatkey))
            return None

    else:
        normmodule = None

    # finally, get the function we need to normalize the light curve
    if normfunc_module and normfunc:
        try:
            normfunc_in = getattr(normmodule, normfunc)
        except AttributeError:
            LOGEXCEPTION('Could not get the specified norm '
                         'function: %s for lcformat: %s '
                         'from module: %s'
                         % (formatkey, normfunc_module, normfunc))
            raise

    else:
        normfunc_in = None


    # add in any optional kwargs that need to be there for readerfunc
    if isinstance(readerfunc_kwargs, dict):
        readerfunc_in = partial(readerfunc_in, **readerfunc_kwargs)

    # add in any optional kwargs that need to be there for normfunc
    if normfunc_in is not None:
        if isinstance(normfunc_kwargs, dict):
            normfunc_in = partial(normfunc_in, **normfunc_kwargs)

    # assemble the return tuple
    # this can be used directly by other lcproc functions
    returntuple = (
        fileglob,
        readerfunc_in,
        timecols,
        magcols,
        errcols,
        magsarefluxes,
        normfunc_in,
    )

    return returntuple