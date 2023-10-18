def perfect_platonic_per_pixel(N, R, scale=11, pos=None, zscale=1.0, returnpix=None):
    """
    Create a perfect platonic sphere of a given radius R by supersampling by a
    factor scale on a grid of size N.  Scale must be odd.

    We are able to perfectly position these particles up to 1/scale. Therefore,
    let's only allow those types of shifts for now, but return the actual position
    used for the placement.
    """
    # enforce odd scale size
    if scale % 2 != 1:
        scale += 1

    if pos is None:
        # place the default position in the center of the grid
        pos = np.array([(N-1)/2.0]*3)

    # limit positions to those that are exact on the size 1./scale
    # positions have the form (d = divisions):
    #   p = N + m/d
    s = 1.0/scale
    f = zscale**2

    i = pos.astype('int')
    p = i + s*((pos - i)/s).astype('int')
    pos = p + 1e-10 # unfortunately needed to break ties

    # make the output arrays
    image = np.zeros((N,)*3)
    x,y,z = np.meshgrid(*(xrange(N),)*3, indexing='ij')

    # for each real pixel in the image, integrate a bunch of superres pixels
    for x0,y0,z0 in zip(x.flatten(),y.flatten(),z.flatten()):

        # short-circuit things that are just too far away!
        ddd = np.sqrt(f*(x0-pos[0])**2 + (y0-pos[1])**2 + (z0-pos[2])**2)
        if ddd > R + 4:
            image[x0,y0,z0] = 0.0
            continue

        # otherwise, build the local mesh and count the volume
        xp,yp,zp = np.meshgrid(
            *(np.linspace(i-0.5+s/2, i+0.5-s/2, scale, endpoint=True) for i in (x0,y0,z0)),
            indexing='ij'
        )
        ddd = np.sqrt(f*(xp-pos[0])**2 + (yp-pos[1])**2 + (zp-pos[2])**2)

        if returnpix is not None and returnpix == [x0,y0,z0]:
            outpix = 1.0 * (ddd < R)

        vol = (1.0*(ddd < R) + 0.0*(ddd == R)).sum()
        image[x0,y0,z0] = vol / float(scale**3)

    #vol_true = 4./3*np.pi*R**3
    #vol_real = image.sum()
    #print vol_true, vol_real, (vol_true - vol_real)/vol_true

    if returnpix:
        return image, pos, outpix
    return image, pos