def fits_finder_chart(
        fitsfile,
        outfile,
        fitsext=0,
        wcsfrom=None,
        scale=ZScaleInterval(),
        stretch=LinearStretch(),
        colormap=plt.cm.gray_r,
        findersize=None,
        finder_coordlimits=None,
        overlay_ra=None,
        overlay_decl=None,
        overlay_pltopts={'marker':'o',
                         'markersize':10.0,
                         'markerfacecolor':'none',
                         'markeredgewidth':2.0,
                         'markeredgecolor':'red'},
        overlay_zoomcontain=False,
        grid=False,
        gridcolor='k'
):
    '''This makes a finder chart for a given FITS with an optional object
    position overlay.

    Parameters
    ----------

    fitsfile : str
        `fitsfile` is the FITS file to use to make the finder chart.

    outfile : str
        `outfile` is the name of the output file. This can be a png or pdf or
        whatever else matplotlib can write given a filename and extension.

    fitsext : int
        Sets the FITS extension in `fitsfile` to use to extract the image array
        from.

    wcsfrom : str or None
        If `wcsfrom` is None, the WCS to transform the RA/Dec to pixel x/y will
        be taken from the FITS header of `fitsfile`. If this is not None, it
        must be a FITS or similar file that contains a WCS header in its first
        extension.

    scale : astropy.visualization.Interval object
        `scale` sets the normalization for the FITS pixel values. This is an
        astropy.visualization Interval object.
        See http://docs.astropy.org/en/stable/visualization/normalization.html
        for details on `scale` and `stretch` objects.

    stretch : astropy.visualization.Stretch object
        `stretch` sets the stretch function for mapping FITS pixel values to
        output pixel values. This is an astropy.visualization Stretch object.
        See http://docs.astropy.org/en/stable/visualization/normalization.html
        for details on `scale` and `stretch` objects.

    colormap : matplotlib Colormap object
        `colormap` is a matplotlib color map object to use for the output image.

    findersize : None or tuple of two ints
        If `findersize` is None, the output image size will be set by the NAXIS1
        and NAXIS2 keywords in the input `fitsfile` FITS header. Otherwise,
        `findersize` must be a tuple with the intended x and y size of the image
        in inches (all output images will use a DPI = 100).

    finder_coordlimits : list of four floats or None
        If not None, `finder_coordlimits` sets x and y limits for the plot,
        effectively zooming it in if these are smaller than the dimensions of
        the FITS image. This should be a list of the form: [minra, maxra,
        mindecl, maxdecl] all in decimal degrees.

    overlay_ra, overlay_decl : np.array or None
        `overlay_ra` and `overlay_decl` are ndarrays containing the RA and Dec
        values to overplot on the image as an overlay. If these are both None,
        then no overlay will be plotted.

    overlay_pltopts : dict
        `overlay_pltopts` controls how the overlay points will be plotted. This
        a dict with standard matplotlib marker, etc. kwargs as key-val pairs,
        e.g. 'markersize', 'markerfacecolor', etc. The default options make red
        outline circles at the location of each object in the overlay.

    overlay_zoomcontain : bool
        `overlay_zoomcontain` controls if the finder chart will be zoomed to
        just contain the overlayed points. Everything outside the footprint of
        these points will be discarded.

    grid : bool
        `grid` sets if a grid will be made on the output image.

    gridcolor : str
        `gridcolor` sets the color of the grid lines. This is a usual matplotib
        color spec string.

    Returns
    -------

    str or None
        The filename of the generated output image if successful. None
        otherwise.

    '''

    # read in the FITS file
    if wcsfrom is None:

        hdulist = pyfits.open(fitsfile)
        img, hdr = hdulist[fitsext].data, hdulist[fitsext].header
        hdulist.close()

        frameshape = (hdr['NAXIS1'], hdr['NAXIS2'])
        w = WCS(hdr)

    elif os.path.exists(wcsfrom):

        hdulist = pyfits.open(fitsfile)
        img, hdr = hdulist[fitsext].data, hdulist[fitsext].header
        hdulist.close()

        frameshape = (hdr['NAXIS1'], hdr['NAXIS2'])
        w = WCS(wcsfrom)

    else:

        LOGERROR('could not determine WCS info for input FITS: %s' %
                 fitsfile)
        return None

    # use the frame shape to set the output PNG's dimensions
    if findersize is None:
        fig = plt.figure(figsize=(frameshape[0]/100.0,
                                  frameshape[1]/100.0))
    else:
        fig = plt.figure(figsize=findersize)


    # set the coord limits if zoomcontain is True
    # we'll leave 30 arcseconds of padding on each side
    if (overlay_zoomcontain and
        overlay_ra is not None and
        overlay_decl is not None):

        finder_coordlimits = [overlay_ra.min()-30.0/3600.0,
                              overlay_ra.max()+30.0/3600.0,
                              overlay_decl.min()-30.0/3600.0,
                              overlay_decl.max()+30.0/3600.0]


    # set the coordinate limits if provided
    if finder_coordlimits and isinstance(finder_coordlimits, (list,tuple)):

        minra, maxra, mindecl, maxdecl = finder_coordlimits
        cntra, cntdecl = (minra + maxra)/2.0, (mindecl + maxdecl)/2.0

        pixelcoords = w.all_world2pix([[minra, mindecl],
                                       [maxra, maxdecl],
                                       [cntra, cntdecl]],1)
        x1, y1, x2, y2 = (int(pixelcoords[0,0]),
                          int(pixelcoords[0,1]),
                          int(pixelcoords[1,0]),
                          int(pixelcoords[1,1]))

        xmin = x1 if x1 < x2 else x2
        xmax = x2 if x2 > x1 else x1

        ymin = y1 if y1 < y2 else y2
        ymax = y2 if y2 > y1 else y1

        # create a new WCS with the same transform but new center coordinates
        whdr = w.to_header()
        whdr['CRPIX1'] = (xmax - xmin)/2
        whdr['CRPIX2'] = (ymax - ymin)/2
        whdr['CRVAL1'] = cntra
        whdr['CRVAL2'] = cntdecl
        whdr['NAXIS1'] = xmax - xmin
        whdr['NAXIS2'] = ymax - ymin
        w = WCS(whdr)

    else:
        xmin, xmax, ymin, ymax = 0, hdr['NAXIS2'], 0, hdr['NAXIS1']

    # add the axes with the WCS projection
    # this should automatically handle subimages because we fix the WCS
    # appropriately above for these
    fig.add_subplot(111,projection=w)

    if scale is not None and stretch is not None:

        norm = ImageNormalize(img,
                              interval=scale,
                              stretch=stretch)

        plt.imshow(img[ymin:ymax,xmin:xmax],
                   origin='lower',
                   cmap=colormap,
                   norm=norm)

    else:

        plt.imshow(img[ymin:ymax,xmin:xmax],
                   origin='lower',
                   cmap=colormap)


    # handle additional options
    if grid:
        plt.grid(color=gridcolor,ls='solid',lw=1.0)

    # handle the object overlay
    if overlay_ra is not None and overlay_decl is not None:

        our_pltopts = dict(
            transform=plt.gca().get_transform('fk5'),
            marker='o',
            markersize=10.0,
            markerfacecolor='none',
            markeredgewidth=2.0,
            markeredgecolor='red',
            rasterized=True,
            linestyle='none'
        )
        if overlay_pltopts is not None and isinstance(overlay_pltopts,
                                                      dict):
            our_pltopts.update(overlay_pltopts)


        plt.gca().set_autoscale_on(False)
        plt.gca().plot(overlay_ra, overlay_decl,
                       **our_pltopts)

    plt.xlabel('Right Ascension [deg]')
    plt.ylabel('Declination [deg]')

    # get the x and y axes objects to fix the ticks
    xax = plt.gca().coords[0]
    yax = plt.gca().coords[1]

    yax.set_major_formatter('d.ddd')
    xax.set_major_formatter('d.ddd')

    # save the figure
    plt.savefig(outfile, dpi=100.0)
    plt.close('all')

    return outfile