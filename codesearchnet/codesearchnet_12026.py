def load_xmatch_external_catalogs(xmatchto, xmatchkeys, outfile=None):
    '''This loads the external xmatch catalogs into a dict for use in an xmatch.

    Parameters
    ----------

    xmatchto : list of str
        This is a list of paths to all the catalog text files that will be
        loaded.

        The text files must be 'CSVs' that use the '|' character as the
        separator betwen columns. These files should all begin with a header in
        JSON format on lines starting with the '#' character. this header will
        define the catalog and contains the name of the catalog and the column
        definitions. Column definitions must have the column name and the numpy
        dtype of the columns (in the same format as that expected for the
        numpy.genfromtxt function). Any line that does not begin with '#' is
        assumed to be part of the columns in the catalog. An example is shown
        below::

            # {"name":"NSVS catalog of variable stars",
            #  "columns":[
            #   {"key":"objectid", "dtype":"U20", "name":"Object ID", "unit": null},
            #   {"key":"ra", "dtype":"f8", "name":"RA", "unit":"deg"},
            #   {"key":"decl","dtype":"f8", "name": "Declination", "unit":"deg"},
            #   {"key":"sdssr","dtype":"f8","name":"SDSS r", "unit":"mag"},
            #   {"key":"vartype","dtype":"U20","name":"Variable type", "unit":null}
            #  ],
            #  "colra":"ra",
            #  "coldec":"decl",
            #  "description":"Contains variable stars from the NSVS catalog"}
            objectid1 | 45.0  | -20.0 | 12.0 | detached EB
            objectid2 | 145.0 | 23.0  | 10.0 | RRab
            objectid3 | 12.0  | 11.0  | 14.0 | Cepheid
            .
            .
            .

    xmatchkeys : list of lists
        This is the list of lists of column names (as str) to get out of each
        `xmatchto` catalog. This should be the same length as `xmatchto` and
        each element here will apply to the respective file in `xmatchto`.

    outfile : str or None
        If this is not None, set this to the name of the pickle to write the
        collected xmatch catalogs to. this pickle can then be loaded
        transparently by the :py:func:`astrobase.checkplot.pkl.checkplot_dict`,
        :py:func:`astrobase.checkplot.pkl.checkplot_pickle` functions to provide
        xmatch info to the
        :py:func:`astrobase.checkplot.pkl_xmatch.xmatch_external_catalogs`
        function below.

        If this is None, will return the loaded xmatch catalogs directly. This
        will be a huge dict, so make sure you have enough RAM.

    Returns
    -------

    str or dict
        Based on the `outfile` kwarg, will either return the path to a collected
        xmatch pickle file or the collected xmatch dict.

    '''

    outdict = {}

    for xc, xk in zip(xmatchto, xmatchkeys):

        parsed_catdef = _parse_xmatch_catalog_header(xc, xk)

        if not parsed_catdef:
            continue

        (infd, catdefdict,
         catcolinds, catcoldtypes,
         catcolnames, catcolunits) = parsed_catdef

        # get the specified columns out of the catalog
        catarr = np.genfromtxt(infd,
                               usecols=catcolinds,
                               names=xk,
                               dtype=','.join(catcoldtypes),
                               comments='#',
                               delimiter='|',
                               autostrip=True)
        infd.close()

        catshortname = os.path.splitext(os.path.basename(xc))[0]
        catshortname = catshortname.replace('.csv','')

        #
        # make a kdtree for this catalog
        #

        # get the ra and decl columns
        objra, objdecl = (catarr[catdefdict['colra']],
                          catarr[catdefdict['coldec']])

        # get the xyz unit vectors from ra,decl
        cosdecl = np.cos(np.radians(objdecl))
        sindecl = np.sin(np.radians(objdecl))
        cosra = np.cos(np.radians(objra))
        sinra = np.sin(np.radians(objra))
        xyz = np.column_stack((cosra*cosdecl,sinra*cosdecl, sindecl))

        # generate the kdtree
        kdt = cKDTree(xyz,copy_data=True)

        # generate the outdict element for this catalog
        catoutdict = {'kdtree':kdt,
                      'data':catarr,
                      'columns':xk,
                      'colnames':catcolnames,
                      'colunits':catcolunits,
                      'name':catdefdict['name'],
                      'desc':catdefdict['description']}

        outdict[catshortname] = catoutdict

    if outfile is not None:

        # if we're on OSX, we apparently need to save the file in chunks smaller
        # than 2 GB to make it work right. can't load pickles larger than 4 GB
        # either, but 3 GB < total size < 4 GB appears to be OK when loading.
        # also see: https://bugs.python.org/issue24658.
        # fix adopted from: https://stackoverflow.com/a/38003910
        if sys.platform == 'darwin':

            dumpbytes = pickle.dumps(outdict, protocol=pickle.HIGHEST_PROTOCOL)
            max_bytes = 2**31 - 1

            with open(outfile, 'wb') as outfd:
                for idx in range(0, len(dumpbytes), max_bytes):
                    outfd.write(dumpbytes[idx:idx+max_bytes])

        else:
            with open(outfile, 'wb') as outfd:
                pickle.dump(outdict, outfd, pickle.HIGHEST_PROTOCOL)

        return outfile

    else:

        return outdict