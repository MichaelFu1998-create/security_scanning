def thr_img(img, thr=2., mode='+'):
    """ Use the given magic function name `func` to threshold with value `thr`
    the data of `img` and return a new nibabel.Nifti1Image.
    Parameters
    ----------
    img: img-like

    thr: float or int
        The threshold value.

    mode: str
        Choices: '+' for positive threshold,
                 '+-' for positive and negative threshold and
                 '-' for negative threshold.
    Returns
    -------
    thr_img: nibabel.Nifti1Image
        Thresholded image
    """

    vol  = read_img(img).get_data()

    if mode == '+':
        mask = vol > thr
    elif mode == '+-' or mode == '-+':
        mask = np.abs(vol) > thr
    elif mode == '-':
        mask = vol < -thr
    else:
        raise ValueError("Expected `mode` to be one of ('+', '+-', '-+', '-'), "
                         "got {}.".format(mode))

    return vol * mask