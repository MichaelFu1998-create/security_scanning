def identify_slab(im, sigma=5., region_size=10, masscut=1e4, asdict=False):
    """
    Identifies slabs in an image.

    Functions by running a Harris-inspired edge detection on the image,
    thresholding the edge, then clustering.

    Parameters
    ----------
        im : numpy.ndarray
            3D array of the image to analyze.
        sigma : Float, optional
            Gaussian blurring kernel to remove non-slab features such as
            noise and particles. Default is 5.
        region_size : Int, optional
            The size of region for Harris corner featuring. Default is 10
        masscut : Float, optional
            The minimum number of pixels for a feature to be identified as
            a slab. Default is 1e4; should be smaller for smaller images.
        asdict : Bool, optional
            Set to True to return a list of dicts, with keys of ``'theta'``
            and ``'phi'`` as rotation angles about the x- and z- axes, and
            of ``'zpos'`` for the z-position, i.e. a list of dicts which
            can be unpacked into a :class:``peri.comp.objs.Slab``

    Returns
    -------
        [poses, normals] : numpy.ndarray
            The positions and normals of each slab in the image; ``poses[i]``
            and ``normals[i]`` are the ``i``th slab. Returned if ``asdict``
            is False
        [list]
            A list of dictionaries. Returned if ``asdict`` is True
    """
    #1. edge detect:
    fim = nd.filters.gaussian_filter(im, sigma)
    trc, det = harris_feature(fim, region_size, to_return='trace-determinant')
    #we want an edge == not a corner, so one eigenvalue is high and
    #one is low compared to the other.
    #So -- trc high, normalized det low:
    dnrm = det / (trc*trc)
    trc_cut = otsu_threshold(trc)
    det_cut = otsu_threshold(dnrm)
    slabs = (trc > trc_cut) & (dnrm < det_cut)
    labeled, nslabs = nd.label(slabs)
    #masscuts:
    masses = [(labeled == i).sum() for i in range(1, nslabs+1)]
    good = np.array([m > masscut for m in masses])
    inds = np.nonzero(good)[0] + 1  #+1 b/c the lowest label is the bkg
    #Slabs are identifiied, now getting the coords:
    poses = np.array(nd.measurements.center_of_mass(trc, labeled, inds))
    #normals from eigenvectors of the covariance matrix
    normals = []
    z = np.arange(im.shape[0]).reshape(-1,1,1).astype('float')
    y = np.arange(im.shape[1]).reshape(1,-1,1).astype('float')
    x = np.arange(im.shape[2]).reshape(1,1,-1).astype('float')
    #We also need to identify the direction of the normal:
    gim = [nd.sobel(fim, axis=i) for i in range(fim.ndim)]
    for i, p in zip(range(1, nslabs+1), poses):
        wts = trc * (labeled == i)
        wts /= wts.sum()
        zc, yc, xc = [xi-pi for xi, pi in zip([z,y,x],p.squeeze())]
        cov = [[np.sum(xi*xj*wts) for xi in [zc,yc,xc]] for xj in [zc,yc,xc]]
        vl, vc = np.linalg.eigh(cov)
        #lowest eigenvalue is the normal:
        normal = vc[:,0]
        #Removing the sign ambiguity:
        gn = np.sum([n*g[tuple(p.astype('int'))] for g,n in zip(gim, normal)])
        normal *= np.sign(gn)
        normals.append(normal)
    if asdict:
        get_theta = lambda n: -np.arctan2(n[1], -n[0])
        get_phi = lambda n: np.arcsin(n[2])
        return [{'zpos':p[0], 'angles':(get_theta(n), get_phi(n))}
                for p, n in zip(poses, normals)]
    else:
        return poses, np.array(normals)