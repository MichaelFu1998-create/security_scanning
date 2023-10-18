def parallel_starfeatures_lcdir(lcdir,
                                outdir,
                                lc_catalog_pickle,
                                neighbor_radius_arcsec,
                                fileglob=None,
                                maxobjects=None,
                                deredden=True,
                                custom_bandpasses=None,
                                lcformat='hat-sql',
                                lcformatdir=None,
                                nworkers=NCPUS,
                                recursive=True):
    '''This runs parallel star feature extraction for a directory of LCs.

    Parameters
    ----------

    lcdir : list of str
        The directory to search for light curves.

    outdir : str
        The output directory where the results will be placed.

    lc_catalog_pickle : str
        The path to a catalog containing at a dict with least:

        - an object ID array accessible with `dict['objects']['objectid']`

        - an LC filename array accessible with `dict['objects']['lcfname']`

        - a `scipy.spatial.KDTree` or `cKDTree` object to use for finding
          neighbors for each object accessible with `dict['kdtree']`

        A catalog pickle of the form needed can be produced using
        :py:func:`astrobase.lcproc.catalogs.make_lclist` or
        :py:func:`astrobase.lcproc.catalogs.filter_lclist`.

    neighbor_radius_arcsec : float
        This indicates the radius in arcsec to search for neighbors for this
        object using the light curve catalog's `kdtree`, `objlist`, `lcflist`,
        and in GAIA.

    fileglob : str
        The UNIX file glob to use to search for the light curves in `lcdir`. If
        None, the default value for the light curve format specified will be
        used.

    maxobjects : int
        The number of objects to process from `lclist`.

    deredden : bool
        This controls if the colors and any color classifications will be
        dereddened using 2MASS DUST.

    custom_bandpasses : dict or None
        This is a dict used to define any custom bandpasses in the
        `in_objectinfo` dict you want to make this function aware of and
        generate colors for. Use the format below for this dict::

            {
            '<bandpass_key_1>':{'dustkey':'<twomass_dust_key_1>',
                                'label':'<band_label_1>'
                                'colors':[['<bandkey1>-<bandkey2>',
                                           '<BAND1> - <BAND2>'],
                                          ['<bandkey3>-<bandkey4>',
                                           '<BAND3> - <BAND4>']]},
            .
            ...
            .
            '<bandpass_key_N>':{'dustkey':'<twomass_dust_key_N>',
                                'label':'<band_label_N>'
                                'colors':[['<bandkey1>-<bandkey2>',
                                           '<BAND1> - <BAND2>'],
                                          ['<bandkey3>-<bandkey4>',
                                           '<BAND3> - <BAND4>']]},
            }

        Where:

        `bandpass_key` is a key to use to refer to this bandpass in the
        `objectinfo` dict, e.g. 'sdssg' for SDSS g band

        `twomass_dust_key` is the key to use in the 2MASS DUST result table for
        reddening per band-pass. For example, given the following DUST result
        table (using http://irsa.ipac.caltech.edu/applications/DUST/)::

            |Filter_name|LamEff |A_over_E_B_V_SandF|A_SandF|A_over_E_B_V_SFD|A_SFD|
            |char       |float  |float             |float  |float           |float|
            |           |microns|                  |mags   |                |mags |
             CTIO U       0.3734              4.107   0.209            4.968 0.253
             CTIO B       0.4309              3.641   0.186            4.325 0.221
             CTIO V       0.5517              2.682   0.137            3.240 0.165
            .
            .
            ...

        The `twomass_dust_key` for 'vmag' would be 'CTIO V'. If you want to
        skip DUST lookup and want to pass in a specific reddening magnitude
        for your bandpass, use a float for the value of
        `twomass_dust_key`. If you want to skip DUST lookup entirely for
        this bandpass, use None for the value of `twomass_dust_key`.

        `band_label` is the label to use for this bandpass, e.g. 'W1' for
        WISE-1 band, 'u' for SDSS u, etc.

        The 'colors' list contains color definitions for all colors you want
        to generate using this bandpass. this list contains elements of the
        form::

            ['<bandkey1>-<bandkey2>','<BAND1> - <BAND2>']

        where the the first item is the bandpass keys making up this color,
        and the second item is the label for this color to be used by the
        frontends. An example::

            ['sdssu-sdssg','u - g']

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

    nworkers : int
        The number of parallel workers to launch.

    Returns
    -------

    dict
        A dict with key:val pairs of the input light curve filename and the
        output star features pickle for each LC processed.

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

        LOGINFO('found %s light curves, getting starfeatures...' %
                len(matching))

        return parallel_starfeatures(matching,
                                     outdir,
                                     lc_catalog_pickle,
                                     neighbor_radius_arcsec,
                                     deredden=deredden,
                                     custom_bandpasses=custom_bandpasses,
                                     maxobjects=maxobjects,
                                     lcformat=lcformat,
                                     lcformatdir=lcformatdir,
                                     nworkers=nworkers)

    else:

        LOGERROR('no light curve files in %s format found in %s' % (lcformat,
                                                                    lcdir))
        return None