def apply_epd_magseries(lcfile,
                        timecol,
                        magcol,
                        errcol,
                        externalparams,
                        lcformat='hat-sql',
                        lcformatdir=None,
                        epdsmooth_sigclip=3.0,
                        epdsmooth_windowsize=21,
                        epdsmooth_func=smooth_magseries_savgol,
                        epdsmooth_extraparams=None):

    '''This applies external parameter decorrelation (EPD) to a light curve.

    Parameters
    ----------

    lcfile : str
        The filename of the light curve file to process.

    timecol,magcol,errcol : str
        The keys in the lcdict produced by your light curve reader function that
        correspond to the times, mags/fluxes, and associated measurement errors
        that will be used as input to the EPD process.

    externalparams : dict or None
        This is a dict that indicates which keys in the lcdict obtained from the
        lcfile correspond to the required external parameters. As with timecol,
        magcol, and errcol, these can be simple keys (e.g. 'rjd') or compound
        keys ('magaperture1.mags'). The dict should look something like::

          {'fsv':'<lcdict key>' array: S values for each observation,
           'fdv':'<lcdict key>' array: D values for each observation,
           'fkv':'<lcdict key>' array: K values for each observation,
           'xcc':'<lcdict key>' array: x coords for each observation,
           'ycc':'<lcdict key>' array: y coords for each observation,
           'bgv':'<lcdict key>' array: sky background for each observation,
           'bge':'<lcdict key>' array: sky background err for each observation,
           'iha':'<lcdict key>' array: hour angle for each observation,
           'izd':'<lcdict key>' array: zenith distance for each observation}

        Alternatively, if these exact keys are already present in the lcdict,
        indicate this by setting externalparams to None.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    epdsmooth_sigclip : float or int or sequence of two floats/ints or None
        This specifies how to sigma-clip the input LC before fitting the EPD
        function to it.

        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    epdsmooth_windowsize : int
        This is the number of LC points to smooth over to generate a smoothed
        light curve that will be used to fit the EPD function.

    epdsmooth_func : Python function
        This sets the smoothing filter function to use. A Savitsky-Golay filter
        is used to smooth the light curve by default. The functions that can be
        used with this kwarg are listed in `varbase.trends`. If you want to use
        your own function, it MUST have the following signature::

                def smoothfunc(mags_array, window_size, **extraparams)

        and return a numpy array of the same size as `mags_array` with the
        smoothed time-series. Any extra params can be provided using the
        `extraparams` dict.

    epdsmooth_extraparams : dict
        This is a dict of any extra filter params to supply to the smoothing
        function.

    Returns
    -------

    str
        Writes the output EPD light curve to a pickle that contains the lcdict
        with an added `lcdict['epd']` key, which contains the EPD times,
        mags/fluxes, and errs as `lcdict['epd']['times']`,
        `lcdict['epd']['mags']`, and `lcdict['epd']['errs']`. Returns the
        filename of this generated EPD LC pickle file.

    Notes
    -----

    - S -> measure of PSF sharpness (~1/sigma^2 sosmaller S = wider PSF)
    - D -> measure of PSF ellipticity in xy direction
    - K -> measure of PSF ellipticity in cross direction

    S, D, K are related to the PSF's variance and covariance, see eqn 30-33 in
    A. Pal's thesis: https://arxiv.org/abs/0906.3486

    '''
    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (dfileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    lcdict = readerfunc(lcfile)
    if ((isinstance(lcdict, (tuple, list))) and
        isinstance(lcdict[0], dict)):
        lcdict = lcdict[0]

    objectid = lcdict['objectid']
    times, mags, errs = lcdict[timecol], lcdict[magcol], lcdict[errcol]

    if externalparams is not None:

        fsv = lcdict[externalparams['fsv']]
        fdv = lcdict[externalparams['fdv']]
        fkv = lcdict[externalparams['fkv']]

        xcc = lcdict[externalparams['xcc']]
        ycc = lcdict[externalparams['ycc']]

        bgv = lcdict[externalparams['bgv']]
        bge = lcdict[externalparams['bge']]

        iha = lcdict[externalparams['iha']]
        izd = lcdict[externalparams['izd']]

    else:

        fsv = lcdict['fsv']
        fdv = lcdict['fdv']
        fkv = lcdict['fkv']

        xcc = lcdict['xcc']
        ycc = lcdict['ycc']

        bgv = lcdict['bgv']
        bge = lcdict['bge']

        iha = lcdict['iha']
        izd = lcdict['izd']

    # apply the corrections for EPD
    epd = epd_magseries(
        times,
        mags,
        errs,
        fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd,
        magsarefluxes=magsarefluxes,
        epdsmooth_sigclip=epdsmooth_sigclip,
        epdsmooth_windowsize=epdsmooth_windowsize,
        epdsmooth_func=epdsmooth_func,
        epdsmooth_extraparams=epdsmooth_extraparams
    )

    # save the EPD magseries to a pickle LC
    lcdict['epd'] = epd
    outfile = os.path.join(
        os.path.dirname(lcfile),
        '%s-epd-%s-pklc.pkl' % (
            squeeze(objectid).replace(' ','-'),
            magcol
        )
    )
    with open(outfile,'wb') as outfd:
        pickle.dump(lcdict, outfd,
                    protocol=pickle.HIGHEST_PROTOCOL)

    return outfile