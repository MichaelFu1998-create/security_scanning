def register_lcformat(formatkey,
                      fileglob,
                      timecols,
                      magcols,
                      errcols,
                      readerfunc_module,
                      readerfunc,
                      readerfunc_kwargs=None,
                      normfunc_module=None,
                      normfunc=None,
                      normfunc_kwargs=None,
                      magsarefluxes=False,
                      overwrite_existing=False,
                      lcformat_dir='~/.astrobase/lcformat-jsons'):
    '''This adds a new LC format to the astrobase LC format registry.

    Allows handling of custom format light curves for astrobase lcproc
    drivers. Once the format is successfully registered, light curves should
    work transparently with all of the functions in this module, by simply
    calling them with the `formatkey` in the `lcformat` keyword argument.

    LC format specifications are generated as JSON files. astrobase comes with
    several of these in `<astrobase install path>/data/lcformats`. LC formats
    you add by using this function will have their specifiers written to the
    `~/.astrobase/lcformat-jsons` directory in your home directory.

    Parameters
    ----------

    formatkey : str
        A str used as the unique ID of this LC format for all lcproc functions
        and can be used to look it up later and import the correct functions
        needed to support it for lcproc operations. For example, we use
        'kep-fits' as a the specifier for Kepler FITS light curves, which can be
        read by the `astrobase.astrokep.read_kepler_fitslc` function as
        specified by the `<astrobase install path>/data/lcformats/kep-fits.json`
        LC format specification JSON produced by `register_lcformat`.

    fileglob : str
        The default UNIX fileglob to use to search for light curve files in this
        LC format. This is a string like '*-whatever-???-*.*??-.lc'.

    timecols,magcols,errcols : list of str
        These are all lists of strings indicating which keys in the lcdict
        produced by your `lcreader_func` that will be extracted and used by
        lcproc functions for processing. The lists must all have the same
        dimensions, e.g. if timecols = ['timecol1','timecol2'], then magcols
        must be something like ['magcol1','magcol2'] and errcols must be
        something like ['errcol1', 'errcol2']. This allows you to process
        multiple apertures or multiple types of measurements in one go.

        Each element in these lists can be a simple key, e.g. 'time' (which
        would correspond to lcdict['time']), or a composite key,
        e.g. 'aperture1.times.rjd' (which would correspond to
        lcdict['aperture1']['times']['rjd']). See the examples in the lcformat
        specification JSON files in `<astrobase install path>/data/lcformats`.

    readerfunc_module : str
        This is either:

        - a Python module import path, e.g. 'astrobase.lcproc.catalogs' or
        - a path to a Python file, e.g. '/astrobase/hatsurveys/hatlc.py'

        that contains the Python module that contains functions used to open
        (and optionally normalize) a custom LC format that's not natively
        supported by astrobase.

    readerfunc : str
        This is the function name in `readerfunc_module` to use to read light
        curves in the custom format. This MUST always return a dictionary (the
        'lcdict') with the following signature (the keys listed below are
        required, but others are allowed)::

            {'objectid': this object's identifier as a string,
             'objectinfo':{'ra': this object's right ascension in decimal deg,
                           'decl': this object's declination in decimal deg,
                           'ndet': the number of observations in this LC,
                           'objectid': the object ID again for legacy reasons},
             ...other time columns, mag columns go in as their own keys}

    normfunc_kwargs : dict or None
        This is a dictionary containing any kwargs to pass through to
        the light curve norm function.

    normfunc_module : str or None
        This is either:

        - a Python module import path, e.g. 'astrobase.lcproc.catalogs' or
        - a path to a Python file, e.g. '/astrobase/hatsurveys/hatlc.py'
        - None, in which case we'll use default normalization

        that contains the Python module that contains functions used to
        normalize a custom LC format that's not natively supported by astrobase.

    normfunc : str or None
        This is the function name in `normfunc_module` to use to normalize light
        curves in the custom format. If None, the default normalization method
        used by lcproc is to find gaps in the time-series, normalize
        measurements grouped by these gaps to zero, then normalize the entire
        magnitude time series to global time series median using the
        `astrobase.lcmath.normalize_magseries` function.

        If this is provided, the normalization function should take and return
        an lcdict of the same form as that produced by `readerfunc` above. For
        an example of a specific normalization function, see
        `normalize_lcdict_by_inst` in the `astrobase.hatsurveys.hatlc` module.

    normfunc_kwargs : dict or None
        This is a dictionary containing any kwargs to pass through to
        the light curve normalization function.

    magsarefluxes : bool
        If this is True, then all lcproc functions will treat the measurement
        columns in the lcdict produced by your `readerfunc` as flux instead of
        mags, so things like default normalization and sigma-clipping will be
        done correctly. If this is False, magnitudes will be treated as
        magnitudes.

    overwrite_existing : bool
        If this is True, this function will overwrite any existing LC format
        specification JSON with the same name as that provided in the
        `formatkey` arg. This can be used to update LC format specifications
        while keeping the `formatkey` the same.

    lcformat_dir : str
        This specifies the directory where the the LC format specification JSON
        produced by this function will be written. By default, this goes to the
        `.astrobase/lcformat-jsons` directory in your home directory.

    Returns
    -------

    str
        Returns the file path to the generated LC format specification JSON
        file.

    '''

    LOGINFO('adding %s to LC format registry...' % formatkey)

    # search for the lcformat_dir and create it if it doesn't exist
    lcformat_dpath = os.path.abspath(
        os.path.expanduser(lcformat_dir)
    )
    if not os.path.exists(lcformat_dpath):
        os.makedirs(lcformat_dpath)

    lcformat_jsonpath = os.path.join(lcformat_dpath,'%s.json' % formatkey)

    if os.path.exists(lcformat_jsonpath) and not overwrite_existing:
        LOGERROR('There is an existing lcformat JSON: %s '
                 'for this formatkey: %s and '
                 'overwrite_existing = False, skipping...'
                 % (lcformat_jsonpath, formatkey))
        return None

    # see if we can import the reader module
    readermodule = _check_extmodule(readerfunc_module, formatkey)

    if not readermodule:
        LOGERROR("could not import the required "
                 "module: %s to read %s light curves" %
                 (readerfunc_module, formatkey))
        return None

    # then, get the function we need to read the light curve
    try:
        getattr(readermodule, readerfunc)
        readerfunc_in = readerfunc
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
            getattr(normmodule, normfunc)
            normfunc_in = normfunc
        except AttributeError:
            LOGEXCEPTION('Could not get the specified norm '
                         'function: %s for lcformat: %s '
                         'from module: %s'
                         % (normfunc, formatkey, normfunc_module))
            raise

    else:
        normfunc_in = None


    # if we made it to here, then everything's good. generate the JSON
    # structure
    formatdict = {'fileglob':fileglob,
                  'timecols':timecols,
                  'magcols':magcols,
                  'errcols':errcols,
                  'magsarefluxes':magsarefluxes,
                  'lcreader_module':readerfunc_module,
                  'lcreader_func':readerfunc_in,
                  'lcreader_kwargs':readerfunc_kwargs,
                  'lcnorm_module':normfunc_module,
                  'lcnorm_func':normfunc_in,
                  'lcnorm_kwargs':normfunc_kwargs}

    # write this to the lcformat directory
    with open(lcformat_jsonpath,'w') as outfd:
        json.dump(formatdict, outfd, indent=4)

    return lcformat_jsonpath