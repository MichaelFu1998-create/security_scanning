def partition_timeseries(image, roi_img, mask_img=None, zeroe=True, roi_values=None, outdict=False):
    """Partition the timeseries in tsvol according to the ROIs in roivol.
    If a mask is given, will use it to exclude any voxel outside of it.

    The outdict indicates whether you want a dictionary for each set of timeseries keyed by the ROI value
    or a list of timeseries sets. If True and roi_img is not None will return an OrderedDict, if False
    or roi_img or roi_list is None will return a list.

    Background value is assumed to be 0 and won't be used here.

    Parameters
    ----------
    image: img-like object or str
        4D timeseries volume

    roi_img: img-like object or str
        3D volume defining different ROIs.

    mask_img: img-like object or str
        3D mask volume

    zeroe: bool
        If true will remove the null timeseries voxels.

    roi_values: list of ROI values (int?)
        List of the values of the ROIs to indicate the
        order and which ROIs will be processed.

    outdict: bool
        If True will return an OrderedDict of timeseries sets, otherwise a list.

    Returns
    -------
    timeseries: list or OrderedDict
        A dict with the timeseries as items and keys as the ROIs voxel values or
        a list where each element is the timeseries set ordered by the sorted values in roi_img or by the roi_values
        argument.

    """
    img  = read_img(image)
    rois = read_img(roi_img)

    # check if roi_img and image are compatible
    check_img_compatibility(img, rois, only_check_3d=True)

    # check if rois has all roi_values
    roi_data = rois.get_data()
    if roi_values is not None:
        for rv in roi_values:
            if not np.any(roi_data == rv):
                raise ValueError('Could not find value {} in rois_img {}.'.format(rv, repr_imgs(roi_img)))
    else:
        roi_values = get_unique_nonzeros(roi_data)

    # check if mask and image are compatible
    if mask_img is None:
        mask_data = None
    else:
        mask = load_mask(mask_img)
        check_img_compatibility(img, mask, only_check_3d=True)
        mask_data = mask.get_data()

    # choose function to call
    if outdict:
        extract_data = _extract_timeseries_dict
    else:
        extract_data = _extract_timeseries_list

    # extract data and return it
    try:
        return extract_data(img.get_data(), rois.get_data(), mask_data,
                            roi_values=roi_values, zeroe=zeroe)
    except:
        raise