def make_lclist(basedir,
                outfile,
                use_list_of_filenames=None,
                lcformat='hat-sql',
                lcformatdir=None,
                fileglob=None,
                recursive=True,
                columns=['objectid',
                         'objectinfo.ra',
                         'objectinfo.decl',
                         'objectinfo.ndet'],
                makecoordindex=('objectinfo.ra','objectinfo.decl'),
                field_fitsfile=None,
                field_wcsfrom=None,
                field_scale=ZScaleInterval(),
                field_stretch=LinearStretch(),
                field_colormap=plt.cm.gray_r,
                field_findersize=None,
                field_pltopts={'marker':'o',
                               'markersize':10.0,
                               'markerfacecolor':'none',
                               'markeredgewidth':2.0,
                               'markeredgecolor':'red'},
                field_grid=False,
                field_gridcolor='k',
                field_zoomcontain=True,
                maxlcs=None,
                nworkers=NCPUS):

    '''This generates a light curve catalog for all light curves in a directory.

    Given a base directory where all the files are, and a light curve format,
    this will find all light curves, pull out the keys in each lcdict requested
    in the `columns` kwarg for each object, and write them to the requested
    output pickle file. These keys should be pointers to scalar values
    (i.e. something like `objectinfo.ra` is OK, but something like 'times' won't
    work because it's a vector).

    Generally, this works with light curve reading functions that produce
    lcdicts as detailed in the docstring for `lcproc.register_lcformat`. Once
    you've registered your light curve reader functions using the
    `lcproc.register_lcformat` function, pass in the `formatkey` associated with
    your light curve format, and this function will be able to read all light
    curves in that format as well as the object information stored in their
    `objectinfo` dict.

    Parameters
    ----------

    basedir : str or list of str
        If this is a str, points to a single directory to search for light
        curves. If this is a list of str, it must be a list of directories to
        search for light curves. All of these will be searched to find light
        curve files matching either your light curve format's default fileglob
        (when you registered your LC format), or a specific fileglob that you
        can pass in using the `fileglob` kwargh here. If the `recursive` kwarg
        is set, the provided directories will be searched recursively.

        If `use_list_of_filenames` is not None, it will override this argument
        and the function will take those light curves as the list of files it
        must process instead of whatever is specified in `basedir`.

    outfile : str
        This is the name of the output file to write. This will be a pickle
        file, so a good convention to use for this name is something like
        'my-lightcurve-catalog.pkl'.

    use_list_of_filenames : list of str or None
        Use this kwarg to override whatever is provided in `basedir` and
        directly pass in a list of light curve files to process. This can speed
        up this function by a lot because no searches on disk will be performed
        to find light curve files matching `basedir` and `fileglob`.

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

    fileglob : str or None
        If provided, is a string that is a valid UNIX filename glob. Used to
        override the default fileglob for this LC format when searching for
        light curve files in `basedir`.

    recursive : bool
        If True, the directories specified in `basedir` will be searched
        recursively for all light curve files that match the default fileglob
        for this LC format or a specific one provided in `fileglob`.

    columns : list of str
        This is a list of keys in the lcdict produced by your light curve reader
        function that contain object information, which will be extracted and
        put into the output light curve catalog. It's highly recommended that
        your LC reader function produce a lcdict that contains at least the
        default keys shown here.

        The lcdict keys to extract are specified by using an address scheme:

        - First level dict keys can be specified directly:
          e.g., 'objectid' will extract lcdict['objectid']
        - Keys at other levels can be specified by using a period to indicate
          the level:

          - e.g., 'objectinfo.ra' will extract lcdict['objectinfo']['ra']
          - e.g., 'objectinfo.varinfo.features.stetsonj' will extract
            lcdict['objectinfo']['varinfo']['features']['stetsonj']

    makecoordindex : list of two str or None
        This is used to specify which lcdict keys contain the right ascension
        and declination coordinates for this object. If these are provided, the
        output light curve catalog will have a kdtree built on all object
        coordinates, which enables fast spatial searches and cross-matching to
        external catalogs by `checkplot` and `lcproc` functions.

    field_fitsfile : str or None
        If this is not None, it should be the path to a FITS image containing
        the objects these light curves are for. If this is provided,
        `make_lclist` will use the WCS information in the FITS itself if
        `field_wcsfrom` is None (or from a WCS header file pointed to by
        `field_wcsfrom`) to obtain x and y pixel coordinates for all of the
        objects in the field. A finder chart will also be made using
        `astrobase.plotbase.fits_finder_chart` using the corresponding
        `field_scale`, `_stretch`, `_colormap`, `_findersize`, `_pltopts`,
        `_grid`, and `_gridcolors` kwargs for that function, reproduced here to
        enable customization of the finder chart plot.

    field_wcsfrom : str or None
        If `wcsfrom` is None, the WCS to transform the RA/Dec to pixel x/y will
        be taken from the FITS header of `fitsfile`. If this is not None, it
        must be a FITS or similar file that contains a WCS header in its first
        extension.

    field_scale : astropy.visualization.Interval object
        `scale` sets the normalization for the FITS pixel values. This is an
        astropy.visualization Interval object.
        See http://docs.astropy.org/en/stable/visualization/normalization.html
        for details on `scale` and `stretch` objects.

    field_stretch : astropy.visualization.Stretch object
        `stretch` sets the stretch function for mapping FITS pixel values to
        output pixel values. This is an astropy.visualization Stretch object.
        See http://docs.astropy.org/en/stable/visualization/normalization.html
        for details on `scale` and `stretch` objects.

    field_colormap : matplotlib Colormap object
        `colormap` is a matplotlib color map object to use for the output image.

    field_findersize : None or tuple of two ints
        If `findersize` is None, the output image size will be set by the NAXIS1
        and NAXIS2 keywords in the input `fitsfile` FITS header. Otherwise,
        `findersize` must be a tuple with the intended x and y size of the image
        in inches (all output images will use a DPI = 100).

    field_pltopts : dict
        `field_pltopts` controls how the overlay points will be plotted. This
        a dict with standard matplotlib marker, etc. kwargs as key-val pairs,
        e.g. 'markersize', 'markerfacecolor', etc. The default options make red
        outline circles at the location of each object in the overlay.

    field_grid : bool
        `grid` sets if a grid will be made on the output image.

    field_gridcolor : str
        `gridcolor` sets the color of the grid lines. This is a usual matplotib
        color spec string.

    field_zoomcontain : bool
        `field_zoomcontain` controls if the finder chart will be zoomed to
        just contain the overlayed points. Everything outside the footprint of
        these points will be discarded.

    maxlcs : int or None
        This sets how many light curves to process in the input LC list
        generated by searching for LCs in `basedir` or in the list provided as
        `use_list_of_filenames`.

    nworkers : int
        This sets the number of parallel workers to launch to collect
        information from the light curves.

    Returns
    -------

    str
        Returns the path to the generated light curve catalog pickle file.

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

    # this is to get the actual ndet
    # set to the magnitudes column
    lcndetkey = dmagcols

    if isinstance(use_list_of_filenames, list):

        matching = use_list_of_filenames

    else:

        # handle the case where basedir is a list of directories
        if isinstance(basedir, list):

            matching = []

            for bdir in basedir:

                # now find the files
                LOGINFO('searching for %s light curves in %s ...' % (lcformat,
                                                                     bdir))

                if recursive is False:
                    matching.extend(glob.glob(os.path.join(bdir, fileglob)))

                else:
                    # use recursive glob for Python 3.5+
                    if sys.version_info[:2] > (3,4):

                        matching.extend(glob.glob(os.path.join(bdir,
                                                               '**',
                                                               fileglob),
                                                  recursive=True))

                    # otherwise, use os.walk and glob
                    else:

                        # use os.walk to go through the directories
                        walker = os.walk(bdir)

                        for root, dirs, _files in walker:
                            for sdir in dirs:
                                searchpath = os.path.join(root,
                                                          sdir,
                                                          fileglob)
                                foundfiles = glob.glob(searchpath)

                                if foundfiles:
                                    matching.extend(foundfiles)


        # otherwise, handle the usual case of one basedir to search in
        else:

            # now find the files
            LOGINFO('searching for %s light curves in %s ...' %
                    (lcformat, basedir))

            if recursive is False:
                matching = glob.glob(os.path.join(basedir, fileglob))

            else:
                # use recursive glob for Python 3.5+
                if sys.version_info[:2] > (3,4):

                    matching = glob.glob(os.path.join(basedir,
                                                      '**',
                                                      fileglob),recursive=True)

                # otherwise, use os.walk and glob
                else:

                    # use os.walk to go through the directories
                    walker = os.walk(basedir)
                    matching = []

                    for root, dirs, _files in walker:
                        for sdir in dirs:
                            searchpath = os.path.join(root,
                                                      sdir,
                                                      fileglob)
                            foundfiles = glob.glob(searchpath)

                            if foundfiles:
                                matching.extend(foundfiles)

    #
    # now that we have all the files, process them
    #
    if matching and len(matching) > 0:

        LOGINFO('found %s light curves' % len(matching))

        # cut down matching to maxlcs
        if maxlcs:
            matching = matching[:maxlcs]

        # prepare the output dict
        lclistdict = {
            'basedir':basedir,
            'lcformat':lcformat,
            'fileglob':fileglob,
            'recursive':recursive,
            'columns':columns,
            'makecoordindex':makecoordindex,
            'nfiles':len(matching),
            'objects': {
            }
        }

        # columns that will always be present in the output lclistdict
        derefcols = ['lcfname']
        derefcols.extend(['%s.ndet' % x.split('.')[-1] for x in lcndetkey])

        for dc in derefcols:
            lclistdict['objects'][dc] = []

        # fill in the rest of the lclist columns from the columns kwarg
        for col in columns:

            # dereference the column
            thiscol = col.split('.')
            thiscol = thiscol[-1]
            lclistdict['objects'][thiscol] = []
            derefcols.append(thiscol)

        # start collecting info
        LOGINFO('collecting light curve info...')

        tasks = [(x, columns, lcformat, lcformatdir, lcndetkey)
                 for x in matching]

        with ProcessPoolExecutor(max_workers=nworkers) as executor:
            results = executor.map(_lclist_parallel_worker, tasks)

        results = [x for x in results]

        # update the columns in the overall dict from the results of the
        # parallel map
        for result in results:
            for xcol in derefcols:
                lclistdict['objects'][xcol].append(result[xcol])

        executor.shutdown()

        # done with collecting info
        # turn all of the lists in the lclistdict into arrays
        for col in lclistdict['objects']:
            lclistdict['objects'][col] = np.array(lclistdict['objects'][col])

        # handle duplicate objectids with different light curves

        uniques, counts = np.unique(lclistdict['objects']['objectid'],
                                    return_counts=True)

        duplicated_objectids = uniques[counts > 1]

        if duplicated_objectids.size > 0:

            # redo the objectid array so it has a bit larger dtype so the extra
            # tag can fit into the field
            dt = lclistdict['objects']['objectid'].dtype.str
            dt = '<U%s' % (
                int(dt.replace('<','').replace('U','').replace('S','')) + 3
            )
            lclistdict['objects']['objectid'] = np.array(
                lclistdict['objects']['objectid'],
                dtype=dt
            )

            for objid in duplicated_objectids:

                objid_inds = np.where(
                    lclistdict['objects']['objectid'] == objid
                )

                # mark the duplicates, assume the first instance is the actual
                # one
                for ncounter, nind in enumerate(objid_inds[0][1:]):
                    lclistdict['objects']['objectid'][nind] = '%s-%s' % (
                        lclistdict['objects']['objectid'][nind],
                        ncounter+2
                    )
                    LOGWARNING(
                        'tagging duplicated instance %s of objectid: '
                        '%s as %s-%s, lightcurve: %s' %
                        (ncounter+2, objid, objid, ncounter+2,
                         lclistdict['objects']['lcfname'][nind])
                    )

        # if we're supposed to make a spatial index, do so
        if (makecoordindex and
            isinstance(makecoordindex, (list, tuple)) and
            len(makecoordindex) == 2):

            try:

                # deref the column names
                racol, declcol = makecoordindex
                racol = racol.split('.')[-1]
                declcol = declcol.split('.')[-1]

                # get the ras and decls
                objra, objdecl = (lclistdict['objects'][racol],
                                  lclistdict['objects'][declcol])

                # get the xyz unit vectors from ra,decl
                # since i had to remind myself:
                # https://en.wikipedia.org/wiki/Equatorial_coordinate_system
                cosdecl = np.cos(np.radians(objdecl))
                sindecl = np.sin(np.radians(objdecl))
                cosra = np.cos(np.radians(objra))
                sinra = np.sin(np.radians(objra))
                xyz = np.column_stack((cosra*cosdecl,sinra*cosdecl, sindecl))

                # generate the kdtree
                kdt = sps.cKDTree(xyz,copy_data=True)

                # put the tree into the dict
                lclistdict['kdtree'] = kdt

                LOGINFO('kdtree generated for (ra, decl): (%s, %s)' %
                        (makecoordindex[0], makecoordindex[1]))

            except Exception as e:
                LOGEXCEPTION('could not make kdtree for (ra, decl): (%s, %s)' %
                             (makecoordindex[0], makecoordindex[1]))
                raise

        # generate the xy pairs if fieldfits is not None
        if field_fitsfile and os.path.exists(field_fitsfile):

            # read in the FITS file
            if field_wcsfrom is None:

                hdulist = pyfits.open(field_fitsfile)
                hdr = hdulist[0].header
                hdulist.close()

                w = WCS(hdr)
                wcsok = True

            elif os.path.exists(field_wcsfrom):

                w = WCS(field_wcsfrom)
                wcsok = True

            else:

                LOGERROR('could not determine WCS info for input FITS: %s' %
                         field_fitsfile)
                wcsok = False

            if wcsok:

                # first, transform the ra/decl to x/y and put these in the
                # lclist output dict
                radecl = np.column_stack((objra, objdecl))
                lclistdict['objects']['framexy'] = w.all_world2pix(
                    radecl,
                    1
                )

                # next, we'll make a PNG plot for the finder
                finder_outfile = os.path.join(
                    os.path.dirname(outfile),
                    os.path.splitext(os.path.basename(outfile))[0] + '.png'
                )

                finder_png = fits_finder_chart(
                    field_fitsfile,
                    finder_outfile,
                    wcsfrom=field_wcsfrom,
                    scale=field_scale,
                    stretch=field_stretch,
                    colormap=field_colormap,
                    findersize=field_findersize,
                    overlay_ra=objra,
                    overlay_decl=objdecl,
                    overlay_pltopts=field_pltopts,
                    overlay_zoomcontain=field_zoomcontain,
                    grid=field_grid,
                    gridcolor=field_gridcolor
                )

                if finder_png is not None:
                    LOGINFO('generated a finder PNG '
                            'with an object position overlay '
                            'for this LC list: %s' % finder_png)


        # write the pickle
        with open(outfile,'wb') as outfd:
            pickle.dump(lclistdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

        LOGINFO('done. LC info -> %s' % outfile)
        return outfile

    else:

        LOGERROR('no files found in %s matching %s' % (basedir, fileglob))
        return None