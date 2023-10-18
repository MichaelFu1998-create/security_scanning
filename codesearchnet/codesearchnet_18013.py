def get_num_px_jtj(s, nparams, decimate=1, max_mem=1e9, min_redundant=20):
    """
    Calculates the number of pixels to use for J at a given memory usage.

    Tries to pick a number of pixels as (size of image / `decimate`).
    However, clips this to a maximum size and minimum size to ensure that
    (1) too much memory isn't used and (2) J has enough elements so that
    the inverse of JTJ will be well-conditioned.

    Parameters
    ----------
        s : :class:`peri.states.State`
            The state on which to calculate J.
        nparams : Int
            The number of parameters that will be included in J.
        decimate : Int, optional
            The amount to decimate the number of pixels in the image by,
            i.e. tries to pick num_px = size of image / decimate.
            Default is 1
        max_mem : Numeric, optional
            The maximum allowed memory, in bytes, for J to occupy at
            double-precision. Default is 1e9.
        min_redundant : Int, optional
            The number of pixels must be at least `min_redundant` *
            `nparams`. If not, an error is raised. Default is 20

    Returns
    -------
        num_px : Int
            The number of pixels at which to calcualte J.
    """
    #1. Max for a given max_mem:
    px_mem = int(max_mem // 8 // nparams) #1 float = 8 bytes
    #2. num_pix for a given redundancy
    px_red = min_redundant*nparams
    #3. And # desired for decimation
    px_dec = s.residuals.size//decimate

    if px_red > px_mem:
        raise RuntimeError('Insufficient max_mem for desired redundancy.')
    num_px = np.clip(px_dec, px_red, px_mem).astype('int')
    return num_px