def pick_rois(rois_img, roi_values, bg_val=0):
    """ Return the `rois_img` only with the ROI values from `roi_values`.
    Parameters
    ----------
    rois_img: niimg-like

    roi_values: list of int or float
        The list of values from rois_img.

    bg_val: int or float
        The background value of `rois_img`.

    Returns
    -------
    subset_rois_img: nibabel.Nifti2Image
    """
    img = read_img(rois_img)
    img_data = img.get_data()

    if bg_val == 0:
        out = np.zeros(img_data.shape, dtype=img_data.dtype)
    else:
        out = np.ones(img_data.shape, dtype=img_data.dtype) * bg_val

    for r in roi_values:
        out[img_data == r] = r

    return nib.Nifti2Image(out, affine=img.affine, header=img.header)