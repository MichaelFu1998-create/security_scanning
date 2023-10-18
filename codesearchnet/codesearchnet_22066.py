def fitimageslice(img, res_x, res_y, xslice, yslice, avg_e_func=None, h5file=None, plot=False):
    """
    Fits a gaussian to a slice of an image *img* specified by *xslice* x-coordinates and *yslice* y-coordinates. *res_x* and *res_y* specify image resolution in x and y. *avg_e_func* is a function that returns the energy of the image as a function of x. It should have the form:

    *avg_e_func(x_1, x_2, h5file, res_y)*

    Fits a gaussian to a slice of an image.

    Parameters
    ----------

    img : array
        Image to be fitted.
    res_x : int
        Image resolution in :math:`x`.
    res_y : int
        Image resolution in :math:`y`.
    xslice : (int, int)
        Slice coordinates in :math:`x`
    yslice : (int, int)
        Slice coordinates in :math:`y`
    avg_e_func : function
        Of the form *avg_e_func(x_1, x_2, h5file, res_y)*, returns the energy of the image as a function of :math:`x`.
    h5file : h5file
        Instance from dataset.
    plot : boolean
        Whether to plot or not.
    """
    # ======================================
    # Extract start and end values
    # (NOT necessarily indices!)
    # ======================================
    x_start = xslice[0]
    x_end   = xslice[1]
    y_start = yslice[0]
    y_end   = yslice[1]

    # ======================================
    # Round to pixel edges.  Pixel edges in
    # px units are at 0.5, 1.5, 2.5, etc.
    # ======================================
    y_low = _np.round(y_start-0.5) + 0.5
    y_high = _np.round(y_end-0.5) + 0.5

    # ======================================
    # Take a strip between edges
    # ======================================
    y_px = linspacestep(1, img.shape[0])
    y_bool = _np.logical_and(y_low < y_px, y_px < y_high)
    strip = img[y_bool, x_start:x_end]

    # ======================================
    # Sum over the strip to get an average
    # ======================================
    histdata = _np.sum(strip, 0)
    xbins = len(histdata)
    x = _np.linspace(1, xbins, xbins)*res_x
    
    # ======================================
    # Fit with a Gaussian to find spot size
    # ======================================
    # plotbool=True
    # plotbool = False
    # varbool  = False
    varbool  = True
    gaussout = _sp.GaussResults(
        x,
        histdata,
        sigma_y    = _np.ones(xbins),
        variance   = varbool,
        background = True,
        p0         = [16000, 0.003, 1e-6, 0]
        )

    if avg_e_func is not None:
        # ======================================
        # Get average energy of strip
        # ======================================
        # Sum to get relative counts of pixels
        relcounts = _np.sum(strip, 1) / _np.float(_np.sum(strip))
        # Integrate each pixel strip
        Eavg = 0
        for i, val in enumerate(linspacestep(y_low, y_high-1)):
            Eavg = Eavg + avg_e_func(val, val+1, h5file, res_y)*relcounts[i]
        return Eavg, gaussout
    else:
        return gaussout