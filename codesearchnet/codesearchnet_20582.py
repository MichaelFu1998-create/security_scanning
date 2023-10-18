def icc_img_to_zscore(icc, center_image=False):
    """ Return a z-scored version of `icc`.
    This function is based on GIFT `icatb_convertImageToZScores` function.
    """
    vol = read_img(icc).get_data()

    v2 = vol[vol != 0]
    if center_image:
        v2 = detrend(v2, axis=0)

    vstd = np.linalg.norm(v2, ord=2) / np.sqrt(np.prod(v2.shape) - 1)

    eps = np.finfo(vstd.dtype).eps
    vol /= (eps + vstd)

    return vol