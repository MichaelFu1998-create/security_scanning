def _extract_timeseries_list(tsvol, roivol, maskvol=None, roi_values=None, zeroe=True):
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
        If true will remove the null timeseries voxels. Only applied to timeseries (4D) data.

    roi_values: list of ROI values (int?)
        List of the values of the ROIs to indicate the
        order and which ROIs will be processed.

    Returns
    -------
    ts_list: list
        A list with the timeseries arrays as items
    """
    _check_for_partition(tsvol, roivol, maskvol)

    if roi_values is None:
        roi_values = get_unique_nonzeros(roivol)

    ts_list = []
    for r in roi_values:
        ts = _partition_data(tsvol, roivol, r, maskvol, zeroe)

        if len(ts) == 0:
            ts = np.zeros(tsvol.shape[-1])

        ts_list.append(ts)

    return ts_list