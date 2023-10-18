def skyview_stamp(ra, decl,
                  survey='DSS2 Red',
                  scaling='Linear',
                  flip=True,
                  convolvewith=None,
                  forcefetch=False,
                  cachedir='~/.astrobase/stamp-cache',
                  timeout=10.0,
                  retry_failed=False,
                  savewcsheader=True,
                  verbose=False):
    '''This downloads a DSS FITS stamp centered on the coordinates specified.

    This wraps the function :py:func:`astrobase.services.skyview.get_stamp`,
    which downloads Digitized Sky Survey stamps in FITS format from the NASA
    SkyView service:

    https://skyview.gsfc.nasa.gov/current/cgi/query.pl

    Also adds some useful operations on top of the FITS file returned.

    Parameters
    ----------

    ra,decl : float
        The center coordinates for the stamp in decimal degrees.

    survey : str
        The survey name to get the stamp from. This is one of the
        values in the 'SkyView Surveys' option boxes on the SkyView
        webpage. Currently, we've only tested using 'DSS2 Red' as the value for
        this kwarg, but the other ones should work in principle.

    scaling : str
        This is the pixel value scaling function to use.

    flip : bool
        Will flip the downloaded image top to bottom. This should usually be
        True because matplotlib and FITS have different image coord origin
        conventions. Alternatively, set this to False and use the
        `origin='lower'` in any call to `matplotlib.pyplot.imshow` when plotting
        this image.

    convolvewith : astropy.convolution Kernel object or None
        If `convolvewith` is an astropy.convolution Kernel object from:

        http://docs.astropy.org/en/stable/convolution/kernels.html

        then, this function will return the stamp convolved with that
        kernel. This can be useful to see effects of wide-field telescopes (like
        the HATNet and HATSouth lenses) degrading the nominal 1 arcsec/px of
        DSS, causing blending of targets and any variability.

    forcefetch : bool
        If True, will disregard any existing cached copies of the stamp already
        downloaded corresponding to the requested center coordinates and
        redownload the FITS from the SkyView service.

    cachedir : str
        This is the path to the astrobase cache directory. All downloaded FITS
        stamps are stored here as .fits.gz files so we can immediately respond
        with the cached copy when a request is made for a coordinate center
        that's already been downloaded.

    timeout : float
        Sets the timeout in seconds to wait for a response from the NASA SkyView
        service.

    retry_failed : bool
        If the initial request to SkyView fails, and this is True, will retry
        until it succeeds.

    savewcsheader : bool
        If this is True, also returns the WCS header of the downloaded FITS
        stamp in addition to the FITS image itself. Useful for projecting object
        coordinates onto image xy coordinates for visualization.

    verbose : bool
        If True, indicates progress.

    Returns
    -------

    tuple or array or None
        This returns based on the value of `savewcsheader`:

        - If `savewcsheader=True`, returns a tuple:
          (FITS stamp image as a numpy array, FITS header)
        - If `savewcsheader=False`, returns only the FITS stamp image as numpy
          array.
        - If the stamp retrieval fails, returns None.

    '''

    stampdict = get_stamp(ra, decl,
                          survey=survey,
                          scaling=scaling,
                          forcefetch=forcefetch,
                          cachedir=cachedir,
                          timeout=timeout,
                          retry_failed=retry_failed,
                          verbose=verbose)
    #
    # DONE WITH FETCHING STUFF
    #
    if stampdict:

        # open the frame
        stampfits = pyfits.open(stampdict['fitsfile'])
        header = stampfits[0].header
        frame = stampfits[0].data
        stampfits.close()

        # finally, we can process the frame
        if flip:
            frame = np.flipud(frame)

        if verbose:
            LOGINFO('fetched stamp successfully for (%.3f, %.3f)'
                    % (ra, decl))


        if convolvewith:

            convolved = aconv.convolve(frame, convolvewith)
            if savewcsheader:
                return convolved, header
            else:
                return convolved

        else:

            if savewcsheader:
                return frame, header
            else:
                return frame

    else:
        LOGERROR('could not fetch the requested stamp for '
                 'coords: (%.3f, %.3f) from survey: %s and scaling: %s'
                 % (ra, decl, survey, scaling))
        return None