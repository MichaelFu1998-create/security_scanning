def runcp(
        pfpickle,
        outdir,
        lcbasedir,
        lcfname=None,
        cprenorm=False,
        lclistpkl=None,
        nbrradiusarcsec=60.0,
        maxnumneighbors=5,
        makeneighborlcs=True,
        fast_mode=False,
        gaia_max_timeout=60.0,
        gaia_mirror=None,
        xmatchinfo=None,
        xmatchradiusarcsec=3.0,
        minobservations=99,
        sigclip=10.0,
        lcformat='hat-sql',
        lcformatdir=None,
        timecols=None,
        magcols=None,
        errcols=None,
        skipdone=False,
        done_callback=None,
        done_callback_args=None,
        done_callback_kwargs=None
):
    '''This makes a checkplot pickle for the given period-finding result pickle
    produced by `lcproc.periodfinding.runpf`.

    Parameters
    ----------

    pfpickle : str or None
        This is the filename of the period-finding result pickle file created by
        `lcproc.periodfinding.runpf`. If this is None, the checkplot will be
        made anyway, but no phased LC information will be collected into the
        output checkplot pickle. This can be useful for just collecting GAIA and
        other external information and making LC plots for an object.

    outdir : str
        This is the directory to which the output checkplot pickle will be
        written.

    lcbasedir : str
        The base directory where this function will look for the light curve
        file associated with the object in the input period-finding result
        pickle file.

    lcfname : str or None
        This is usually None because we'll get the path to the light curve
        associated with this period-finding pickle from the pickle itself. If
        `pfpickle` is None, however, this function will use `lcfname` to look up
        the light curve file instead. If both are provided, the value of
        `lcfname` takes precedence.

        Providing the light curve file name in this kwarg is useful when you're
        making checkplots directly from light curve files and not including
        period-finder results (perhaps because period-finding takes a long time
        for large collections of LCs).

    cprenorm : bool
        Set this to True if the light curves should be renormalized by
        `checkplot.checkplot_pickle`. This is set to False by default because we
        do our own normalization in this function using the light curve's
        registered normalization function and pass the normalized times, mags,
        errs to the `checkplot.checkplot_pickle` function.

    lclistpkl : str or dict
        This is either the filename of a pickle or the actual dict produced by
        lcproc.make_lclist. This is used to gather neighbor information.

    nbrradiusarcsec : float
        The radius in arcseconds to use for a search conducted around the
        coordinates of this object to look for any potential confusion and
        blending of variability amplitude caused by their proximity.

    maxnumneighbors : int
        The maximum number of neighbors that will have their light curves and
        magnitudes noted in this checkplot as potential blends with the target
        object.

    makeneighborlcs : bool
        If True, will make light curve and phased light curve plots for all
        neighbors to the current object found in the catalog passed in using
        `lclistpkl`.

    fast_mode : bool or float
        This runs the external catalog operations in a "fast" mode, with short
        timeouts and not trying to hit external catalogs that take a long time
        to respond.

        If this is set to True, the default settings for the external requests
        will then become::

                skyview_lookup = False
                skyview_timeout = 10.0
                skyview_retry_failed = False
                dust_timeout = 10.0
                gaia_submit_timeout = 7.0
                gaia_max_timeout = 10.0
                gaia_submit_tries = 2
                complete_query_later = False
                search_simbad = False

        If this is a float, will run in "fast" mode with the provided timeout
        value in seconds and the following settings::

                skyview_lookup = True
                skyview_timeout = fast_mode
                skyview_retry_failed = False
                dust_timeout = fast_mode
                gaia_submit_timeout = 0.66*fast_mode
                gaia_max_timeout = fast_mode
                gaia_submit_tries = 2
                complete_query_later = False
                search_simbad = False

    gaia_max_timeout : float
        Sets the timeout in seconds to use when waiting for the GAIA service to
        respond to our request for the object's information. Note that if
        `fast_mode` is set, this is ignored.

    gaia_mirror : str or None
        This sets the GAIA mirror to use. This is a key in the
        `services.gaia.GAIA_URLS` dict which defines the URLs to hit for each
        mirror.

    xmatchinfo : str or dict
        This is either the xmatch dict produced by the function
        `load_xmatch_external_catalogs` above, or the path to the xmatch info
        pickle file produced by that function.

    xmatchradiusarcsec : float
        This is the cross-matching radius to use in arcseconds.

    minobservations : int
        The minimum of observations the input object's mag/flux time-series must
        have for this function to plot its light curve and phased light
        curve. If the object has less than this number, no light curves will be
        plotted, but the checkplotdict will still contain all of the other
        information.

    sigclip : float or int or sequence of two floats/ints or None
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

    timecols : list of str or None
        The timecol keys to use from the lcdict in generating this checkplot.

    magcols : list of str or None
        The magcol keys to use from the lcdict in generating this checkplot.

    errcols : list of str or None
        The errcol keys to use from the lcdict in generating this checkplot.

    skipdone : bool
        This indicates if this function will skip creating checkplots that
        already exist corresponding to the current `objectid` and `magcol`. If
        `skipdone` is set to True, this will be done.

    done_callback : Python function or None
        This is used to provide a function to execute after the checkplot
        pickles are generated. This is useful if you want to stream the results
        of checkplot making to some other process, e.g. directly running an
        ingestion into an LCC-Server collection. The function will always get
        the list of the generated checkplot pickles as its first arg, and all of
        the kwargs for runcp in the kwargs dict. Additional args and kwargs can
        be provided by giving a list in the `done_callbacks_args` kwarg and a
        dict in the `done_callbacks_kwargs` kwarg.

        NOTE: the function you pass in here should be pickleable by normal
        Python if you want to use it with the parallel_cp and parallel_cp_lcdir
        functions below.

    done_callback_args : tuple or None
        If not None, contains any args to pass into the `done_callback`
        function.

    done_callback_kwargs : dict or None
        If not None, contains any kwargs to pass into the `done_callback`
        function.

    Returns
    -------

    list of str
        This returns a list of checkplot pickle filenames with one element for
        each (timecol, magcol, errcol) combination provided in the default
        lcformat config or in the timecols, magcols, errcols kwargs.

    '''

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (fileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    if pfpickle is not None:

        if pfpickle.endswith('.gz'):
            infd = gzip.open(pfpickle,'rb')
        else:
            infd = open(pfpickle,'rb')

        pfresults = pickle.load(infd)

        infd.close()


    # override the default timecols, magcols, and errcols
    # using the ones provided to the function
    if timecols is None:
        timecols = dtimecols
    if magcols is None:
        magcols = dmagcols
    if errcols is None:
        errcols = derrcols

    if ((lcfname is not None or pfpickle is None) and os.path.exists(lcfname)):

        lcfpath = lcfname
        objectid = None

    else:

        if pfpickle is not None:

            objectid = pfresults['objectid']
            lcfbasename = pfresults['lcfbasename']
            lcfsearchpath = os.path.join(lcbasedir, lcfbasename)

            if os.path.exists(lcfsearchpath):
                lcfpath = lcfsearchpath

            elif lcfname is not None and os.path.exists(lcfname):
                lcfpath = lcfname

            else:
                LOGERROR('could not find light curve for '
                         'pfresult %s, objectid %s, '
                         'used search path: %s, lcfname kwarg: %s' %
                         (pfpickle, objectid, lcfsearchpath, lcfname))
                return None

        else:

            LOGERROR("no light curve provided and pfpickle is None, "
                     "can't continue")
            return None

    lcdict = readerfunc(lcfpath)

    # this should handle lists/tuples being returned by readerfunc
    # we assume that the first element is the actual lcdict
    # FIXME: figure out how to not need this assumption
    if ( (isinstance(lcdict, (list, tuple))) and
         (isinstance(lcdict[0], dict)) ):
        lcdict = lcdict[0]

    # get the object ID from the light curve if pfpickle is None or we used
    # lcfname directly
    if objectid is None:

        if 'objectid' in lcdict:
            objectid = lcdict['objectid']
        elif ('objectid' in lcdict['objectinfo'] and
              lcdict['objectinfo']['objectid']):
            objectid = lcdict['objectinfo']['objectid']
        elif 'hatid' in lcdict['objectinfo'] and lcdict['objectinfo']['hatid']:
            objectid = lcdict['objectinfo']['hatid']
        else:
            objectid = uuid.uuid4().hex[:5]
            LOGWARNING('no objectid found for this object, '
                       'generated a random one: %s' % objectid)

    # normalize using the special function if specified
    if normfunc is not None:
        lcdict = normfunc(lcdict)

    cpfs = []

    for tcol, mcol, ecol in zip(timecols, magcols, errcols):

        # dereference the columns and get them from the lcdict
        if '.' in tcol:
            tcolget = tcol.split('.')
        else:
            tcolget = [tcol]
        times = _dict_get(lcdict, tcolget)

        if '.' in mcol:
            mcolget = mcol.split('.')
        else:
            mcolget = [mcol]
        mags = _dict_get(lcdict, mcolget)

        if '.' in ecol:
            ecolget = ecol.split('.')
        else:
            ecolget = [ecol]
        errs = _dict_get(lcdict, ecolget)

        # get all the period-finder results from this magcol
        if pfpickle is not None:

            if 'pfmethods' in pfresults[mcol]:
                pflist = [
                    pfresults[mcol][x] for x in
                    pfresults[mcol]['pfmethods'] if
                    len(pfresults[mcol][x].keys()) > 0
                ]
            else:
                pflist = []
                for pfm in PFMETHODS:
                    if (pfm in pfresults[mcol] and
                        len(pfresults[mcol][pfm].keys()) > 0):
                        pflist.append(pfresults[mcol][pfm])

        # special case of generating a checkplot with no phased LCs
        else:
            pflist = []

        # generate the output filename
        outfile = os.path.join(outdir,
                               'checkplot-%s-%s.pkl' % (
                                   squeeze(objectid).replace(' ','-'),
                                   mcol
                               ))

        if skipdone and os.path.exists(outfile):
            LOGWARNING('skipdone = True and '
                       'checkplot for this objectid/magcol combination '
                       'exists already: %s, skipping...' % outfile)
            return outfile

        # make sure the checkplot has a valid objectid
        if 'objectid' not in lcdict['objectinfo']:
            lcdict['objectinfo']['objectid'] = objectid

        # normalize here if not using special normalization
        if normfunc is None:
            ntimes, nmags = normalize_magseries(
                times, mags,
                magsarefluxes=magsarefluxes
            )
            xtimes, xmags, xerrs = ntimes, nmags, errs
        else:
            xtimes, xmags, xerrs = times, mags, errs

        # generate the checkplotdict
        cpd = checkplot_dict(
            pflist,
            xtimes, xmags, xerrs,
            objectinfo=lcdict['objectinfo'],
            gaia_max_timeout=gaia_max_timeout,
            gaia_mirror=gaia_mirror,
            lclistpkl=lclistpkl,
            nbrradiusarcsec=nbrradiusarcsec,
            maxnumneighbors=maxnumneighbors,
            xmatchinfo=xmatchinfo,
            xmatchradiusarcsec=xmatchradiusarcsec,
            sigclip=sigclip,
            mindet=minobservations,
            verbose=False,
            fast_mode=fast_mode,
            magsarefluxes=magsarefluxes,
            normto=cprenorm  # we've done the renormalization already, so this
                             # should be False by default. just messes up the
                             # plots otherwise, destroying LPVs in particular
        )

        if makeneighborlcs:

            # include any neighbor information as well
            cpdupdated = update_checkplotdict_nbrlcs(
                cpd,
                tcol, mcol, ecol,
                lcformat=lcformat,
                verbose=False
            )

        else:

            cpdupdated = cpd

        # write the update checkplot dict to disk
        cpf = _write_checkplot_picklefile(
            cpdupdated,
            outfile=outfile,
            protocol=pickle.HIGHEST_PROTOCOL,
            outgzip=False
        )

        cpfs.append(cpf)

    #
    # done with checkplot making
    #

    LOGINFO('done with %s -> %s' % (objectid, repr(cpfs)))
    if done_callback is not None:

        if (done_callback_args is not None and
            isinstance(done_callback_args,list)):
            done_callback_args = tuple([cpfs] + done_callback_args)

        else:
            done_callback_args = (cpfs,)

        if (done_callback_kwargs is not None and
            isinstance(done_callback_kwargs, dict)):
            done_callback_kwargs.update(dict(
                fast_mode=fast_mode,
                lcfname=lcfname,
                cprenorm=cprenorm,
                lclistpkl=lclistpkl,
                nbrradiusarcsec=nbrradiusarcsec,
                maxnumneighbors=maxnumneighbors,
                gaia_max_timeout=gaia_max_timeout,
                gaia_mirror=gaia_mirror,
                xmatchinfo=xmatchinfo,
                xmatchradiusarcsec=xmatchradiusarcsec,
                minobservations=minobservations,
                sigclip=sigclip,
                lcformat=lcformat,
                fileglob=fileglob,
                readerfunc=readerfunc,
                normfunc=normfunc,
                magsarefluxes=magsarefluxes,
                timecols=timecols,
                magcols=magcols,
                errcols=errcols,
                skipdone=skipdone,
            ))

        else:
            done_callback_kwargs = dict(
                fast_mode=fast_mode,
                lcfname=lcfname,
                cprenorm=cprenorm,
                lclistpkl=lclistpkl,
                nbrradiusarcsec=nbrradiusarcsec,
                maxnumneighbors=maxnumneighbors,
                gaia_max_timeout=gaia_max_timeout,
                gaia_mirror=gaia_mirror,
                xmatchinfo=xmatchinfo,
                xmatchradiusarcsec=xmatchradiusarcsec,
                minobservations=minobservations,
                sigclip=sigclip,
                lcformat=lcformat,
                fileglob=fileglob,
                readerfunc=readerfunc,
                normfunc=normfunc,
                magsarefluxes=magsarefluxes,
                timecols=timecols,
                magcols=magcols,
                errcols=errcols,
                skipdone=skipdone,
            )

        # fire the callback
        try:
            done_callback(*done_callback_args, **done_callback_kwargs)
            LOGINFO('callback fired successfully for %r' % cpfs)
        except Exception as e:
            LOGEXCEPTION('callback function failed for %r' % cpfs)

    # at the end, return the list of checkplot files generated
    return cpfs