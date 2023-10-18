def serial_starfeatures(lclist,
                        outdir,
                        lc_catalog_pickle,
                        neighbor_radius_arcsec,
                        maxobjects=None,
                        deredden=True,
                        custom_bandpasses=None,
                        lcformat='hat-sql',
                        lcformatdir=None):
    '''This drives the `get_starfeatures` function for a collection of LCs.

    Parameters
    ----------

    lclist : list of str
        The list of light curve file names to process.

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

    Returns
    -------

    list of str
        A list of all star features pickles produced.

    '''
    # make sure to make the output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if maxobjects:
        lclist = lclist[:maxobjects]

    # read in the kdtree pickle
    with open(lc_catalog_pickle, 'rb') as infd:
        kdt_dict = pickle.load(infd)

    kdt = kdt_dict['kdtree']
    objlist = kdt_dict['objects']['objectid']
    objlcfl = kdt_dict['objects']['lcfname']

    tasks = [(x, outdir, kdt, objlist, objlcfl,
              neighbor_radius_arcsec,
              deredden, custom_bandpasses,
              lcformat, lcformatdir) for x in lclist]

    for task in tqdm(tasks):
        result = _starfeatures_worker(task)

    return result