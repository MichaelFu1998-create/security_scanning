def filter_icc(icc, mask=None, thr=2, zscore=True, mode="+"):
    """ Threshold then mask an IC correlation map.
    Parameters
    ----------
    icc: img-like
        The 'raw' ICC map.

    mask: img-like
        If not None. Will apply this masks in the end of the process.

    thr: float
        The threshold value.

    zscore: bool
        If True will calculate the z-score of the ICC before thresholding.

    mode: str
        Choices: '+' for positive threshold,
                 '+-' for positive and negative threshold and
                 '-' for negative threshold.

    Returns
    -------
    icc_filt: nibabel.NiftiImage
        Thresholded and masked ICC.
    """
    if zscore:
        icc_filt = thr_img(icc_img_to_zscore(icc), thr=thr, mode=mode)
    else:
        icc_filt = thr_img(icc, thr=thr, mode=mode)

    if mask is not None:
        icc_filt = apply_mask(icc_filt, mask)

    return icc_filt