def parallel_pf_lcdir(lcdir,
                      outdir,
                      fileglob=None,
                      recursive=True,
                      timecols=None,
                      magcols=None,
                      errcols=None,
                      lcformat='hat-sql',
                      lcformatdir=None,
                      pfmethods=('gls','pdm','mav','win'),
                      pfkwargs=({},{},{},{}),
                      sigclip=10.0,
                      getblssnr=False,
                      nperiodworkers=NCPUS,
                      ncontrolworkers=1,
                      liststartindex=None,
                      listmaxobjects=None,
                      minobservations=500,
                      excludeprocessed=True):
    '''This runs parallel light curve period finding for directory of LCs.

    Parameters
    ----------

    lcdir : str
        The directory containing the LCs to process.

    outdir : str
        The directory where the resulting period-finding pickles will go.

    fileglob : str or None
        The UNIX file glob to use to search for LCs in `lcdir`. If None, the
        default file glob associated with the registered LC format will be used
        instead.

    recursive : bool
        If True, will search recursively in `lcdir` for light curves to process.

    timecols : list of str or None
        The timecol keys to use from the lcdict in calculating the features.

    magcols : list of str or None
        The magcol keys to use from the lcdict in calculating the features.

    errcols : list of str or None
        The errcol keys to use from the lcdict in calculating the features.

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

    pfmethods : list of str
        This is a list of period finding methods to run. Each element is a
        string matching the keys of the `PFMETHODS` dict above. By default, this
        runs GLS, PDM, AoVMH, and the spectral window Lomb-Scargle periodogram.

    pfkwargs : list of dicts
        This is used to provide any special kwargs as dicts to each
        period-finding method function specified in `pfmethods`.

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

    getblssnr : bool
        If this is True and BLS is one of the methods specified in `pfmethods`,
        will also calculate the stats for each best period in the BLS results:
        transit depth, duration, ingress duration, refit period and epoch, and
        the SNR of the transit.

    nperiodworkers : int
        The number of parallel period-finding workers to launch per object task.

    ncontrolworkers : int
        The number of controlling processes to launch. This effectively sets how
        many objects from `lclist` will be processed in parallel.

    liststartindex : int or None
        This sets the index from where to start in `lclist`.

    listmaxobjects : int or None
        This sets the maximum number of objects in `lclist` to run
        period-finding for in this invocation. Together with `liststartindex`,
        `listmaxobjects` can be used to distribute processing over several
        independent machines if the number of light curves is very large.

    minobservations : int
        The minimum number of finite LC points required to process a light
        curve.

    excludeprocessed : bool
        If this is True, light curves that have existing period-finding result
        pickles in `outdir` will not be processed.

        FIXME: currently, this uses a dumb method of excluding already-processed
        files. A smarter way to do this is to (i) generate a SHA512 cachekey
        based on a repr of `{'lcfile', 'timecols', 'magcols', 'errcols',
        'lcformat', 'pfmethods', 'sigclip', 'getblssnr', 'pfkwargs'}`, (ii) make
        sure all list kwargs in the dict are sorted, (iii) check if the output
        file has the same cachekey in its filename (last 8 chars of cachekey
        should work), so the result was processed in exactly the same way as
        specifed in the input to this function, and can therefore be
        ignored. Will implement this later.

    Returns
    -------

    list of str
        A list of the period-finding pickles created for all of input LCs
        processed.

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

    if not fileglob:
        fileglob = dfileglob

    # now find the files
    LOGINFO('searching for %s light curves in %s ...' % (lcformat, lcdir))

    if recursive is False:
        matching = glob.glob(os.path.join(lcdir, fileglob))

    else:
        # use recursive glob for Python 3.5+
        if sys.version_info[:2] > (3,4):

            matching = glob.glob(os.path.join(lcdir,
                                              '**',
                                              fileglob),recursive=True)

        # otherwise, use os.walk and glob
        else:

            # use os.walk to go through the directories
            walker = os.walk(lcdir)
            matching = []

            for root, dirs, _files in walker:
                for sdir in dirs:
                    searchpath = os.path.join(root,
                                              sdir,
                                              fileglob)
                    foundfiles = glob.glob(searchpath)

                    if foundfiles:
                        matching.extend(foundfiles)


    # now that we have all the files, process them
    if matching and len(matching) > 0:

        # this helps us process things in deterministic order when we distribute
        # processing over several machines
        matching = sorted(matching)

        LOGINFO('found %s light curves, running pf...' % len(matching))

        return parallel_pf(matching,
                           outdir,
                           timecols=timecols,
                           magcols=magcols,
                           errcols=errcols,
                           lcformat=lcformat,
                           lcformatdir=lcformatdir,
                           pfmethods=pfmethods,
                           pfkwargs=pfkwargs,
                           getblssnr=getblssnr,
                           sigclip=sigclip,
                           nperiodworkers=nperiodworkers,
                           ncontrolworkers=ncontrolworkers,
                           liststartindex=liststartindex,
                           listmaxobjects=listmaxobjects,
                           minobservations=minobservations,
                           excludeprocessed=excludeprocessed)

    else:

        LOGERROR('no light curve files in %s format found in %s' % (lcformat,
                                                                    lcdir))
        return None