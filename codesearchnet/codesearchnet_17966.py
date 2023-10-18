def wrap_and_calc_psf(xpts, ypts, zpts, func, **kwargs):
    """
    Wraps a point-spread function in x and y.

    Speeds up psf calculations by a factor of 4 for free / some broadcasting
    by exploiting the x->-x, y->-y symmetry of a psf function. Pass x and y
    as the positive (say) values of the coordinates at which to evaluate func,
    and it will return the function sampled at [x[::-1]] + x. Note it is not
    wrapped in z.

    Parameters
    ----------
        xpts : numpy.ndarray
            1D N-element numpy.array of the x-points to evaluate func at.
        ypts : numpy.ndarray
            y-points to evaluate func at.
        zpts : numpy.ndarray
            z-points to evaluate func at.
        func : function
            The function to evaluate and wrap around. Syntax must be
            func(x,y,z, **kwargs)
        **kwargs : Any parameters passed to the function.

    Outputs
    -------
        to_return : numpy.ndarray
            The wrapped and calculated psf, of shape
            [2*x.size - x0, 2*y.size - y0, z.size], where x0=1 if x[0]=0, etc.

    Notes
    -----
    The coordinates should be something like numpy.arange(start, stop, diff),
    with start near 0. If x[0]==0, all of x is calcualted but only x[1:]
    is wrapped (i.e. it works whether or not x[0]=0).

    This doesn't work directly for a linescan psf because the illumination
    portion is not like a grid. However, the illumination and detection
    are already combined with wrap_and_calc in calculate_linescan_psf etc.
    """
    #1. Checking that everything is hunky-dory:
    for t in [xpts,ypts,zpts]:
        if len(t.shape) != 1:
            raise ValueError('xpts,ypts,zpts must be 1D.')

    dx = 1 if xpts[0]==0 else 0
    dy = 1 if ypts[0]==0 else 0

    xg,yg,zg = np.meshgrid(xpts,ypts,zpts, indexing='ij')
    xs, ys, zs = [ pts.size for pts in [xpts,ypts,zpts] ]
    to_return = np.zeros([2*xs-dx, 2*ys-dy, zs])

    #2. Calculate:
    up_corner_psf = func(xg,yg,zg, **kwargs)

    to_return[xs-dx:,ys-dy:,:] = up_corner_psf.copy()                     #x>0, y>0
    if dx == 0:
        to_return[:xs-dx,ys-dy:,:] = up_corner_psf[::-1,:,:].copy()       #x<0, y>0
    else:
        to_return[:xs-dx,ys-dy:,:] = up_corner_psf[-1:0:-1,:,:].copy()    #x<0, y>0
    if dy == 0:
        to_return[xs-dx:,:ys-dy,:] = up_corner_psf[:,::-1,:].copy()       #x>0, y<0
    else:
        to_return[xs-dx:,:ys-dy,:] = up_corner_psf[:,-1:0:-1,:].copy()    #x>0, y<0
    if (dx == 0) and (dy == 0):
        to_return[:xs-dx,:ys-dy,:] = up_corner_psf[::-1,::-1,:].copy()    #x<0,y<0
    elif (dx == 0) and (dy != 0):
        to_return[:xs-dx,:ys-dy,:] = up_corner_psf[::-1,-1:0:-1,:].copy() #x<0,y<0
    elif (dy == 0) and (dx != 0):
        to_return[:xs-dx,:ys-dy,:] = up_corner_psf[-1:0:-1,::-1,:].copy() #x<0,y<0
    else: #dx==1 and dy==1
        to_return[:xs-dx,:ys-dy,:] = up_corner_psf[-1:0:-1,-1:0:-1,:].copy()#x<0,y<0

    return to_return