def _extract_timeseries_dict(tsvol, roivol, maskvol=None, roi_values=None, zeroe=True):
    """Partition the timeseries in tsvol according to the ROIs in roivol.
    If a mask is given, will use it to exclude any voxel outside of it.

    Parameters
    ----------
    tsvol: numpy.ndarray
        4D timeseries volume or a 3D volume to be partitioned

    roivol: numpy.ndarray
        3D ROIs volume

    maskvol: numpy.ndarray
        3D mask volume

    zeroe: bool
        If true will remove the null timeseries voxels.

    roi_values: list of ROI values (int?)
        List of the values of the ROIs to indicate the
        order and which ROIs will be processed.

    Returns
    -------
    ts_dict: OrderedDict
        A dict with the timeseries as items and keys as the ROIs voxel values.
    """
    _check_for_partition(tsvol, roivol, maskvol)

    # get unique values of the atlas
    if roi_values is None:
        roi_values = get_unique_nonzeros(roivol)

    ts_dict = OrderedDict()
    for r in roi_values:
        ts = _partition_data(tsvol, roivol, r, maskvol, zeroe)

        if len(ts) == 0:
            ts = np.zeros(tsvol.shape[-1])

        ts_dict[r] = ts

    return ts_dict