def get_starfeatures(lcfile,
                     outdir,
                     kdtree,
                     objlist,
                     lcflist,
                     neighbor_radius_arcsec,
                     deredden=True,
                     custom_bandpasses=None,
                     lcformat='hat-sql',
                     lcformatdir=None):
    '''This runs the functions from :py:func:`astrobase.varclass.starfeatures`
    on a single light curve file.

    Parameters
    ----------

    lcfile : str
        This is the LC file to extract star features for.

    outdir : str
        This is the directory to write the output pickle to.

    kdtree: scipy.spatial.cKDTree
        This is a `scipy.spatial.KDTree` or `cKDTree` used to calculate neighbor
        proximity features. This is for the light curve catalog this object is
        in.

    objlist : np.array
        This is a Numpy array of object IDs in the same order as the
        `kdtree.data` np.array. This is for the light curve catalog this object
        is in.

    lcflist : np.array
        This is a Numpy array of light curve filenames in the same order as
        `kdtree.data`. This is for the light curve catalog this object is in.

    neighbor_radius_arcsec : float
        This indicates the radius in arcsec to search for neighbors for this
        object using the light curve catalog's `kdtree`, `objlist`, `lcflist`,
        and in GAIA.

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

    str
        Path to the output pickle containing all of the star features for this
        object.

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

    try:

        # get the LC into a dict
        lcdict = readerfunc(lcfile)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]

        resultdict = {'objectid':lcdict['objectid'],
                      'info':lcdict['objectinfo'],
                      'lcfbasename':os.path.basename(lcfile)}

        # run the coord features first
        coordfeat = starfeatures.coord_features(lcdict['objectinfo'])

        # next, run the color features
        colorfeat = starfeatures.color_features(
            lcdict['objectinfo'],
            deredden=deredden,
            custom_bandpasses=custom_bandpasses
        )

        # run a rough color classification
        colorclass = starfeatures.color_classification(colorfeat,
                                                       coordfeat)

        # finally, run the neighbor features
        nbrfeat = starfeatures.neighbor_gaia_features(lcdict['objectinfo'],
                                                      kdtree,
                                                      neighbor_radius_arcsec)

        # get the objectids of the neighbors found if any
        if nbrfeat['nbrindices'].size > 0:
            nbrfeat['nbrobjectids'] = objlist[nbrfeat['nbrindices']]
            nbrfeat['closestnbrobjectid'] = objlist[
                nbrfeat['closestdistnbrind']
            ]
            nbrfeat['closestnbrlcfname'] = lcflist[
                nbrfeat['closestdistnbrind']
            ]

        else:
            nbrfeat['nbrobjectids'] = np.array([])
            nbrfeat['closestnbrobjectid'] = np.array([])
            nbrfeat['closestnbrlcfname'] = np.array([])

        # update the result dict
        resultdict.update(coordfeat)
        resultdict.update(colorfeat)
        resultdict.update(colorclass)
        resultdict.update(nbrfeat)

        outfile = os.path.join(outdir,
                               'starfeatures-%s.pkl' %
                               squeeze(resultdict['objectid']).replace(' ','-'))

        with open(outfile, 'wb') as outfd:
            pickle.dump(resultdict, outfd, protocol=4)

        return outfile

    except Exception as e:

        LOGEXCEPTION('failed to get star features for %s because: %s' %
                     (os.path.basename(lcfile), e))
        return None