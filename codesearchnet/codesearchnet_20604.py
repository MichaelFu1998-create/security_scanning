def _partition_data(datavol, roivol, roivalue, maskvol=None, zeroe=True):
    """ Extracts the values in `datavol` that are in the ROI with value `roivalue` in `roivol`.
    The ROI can be masked by `maskvol`.

    Parameters
    ----------
    datavol: numpy.ndarray
        4D timeseries volume or a 3D volume to be partitioned

    roivol: numpy.ndarray
        3D ROIs volume

    roivalue: int or float
        A value from roivol that represents the ROI to be used for extraction.

    maskvol: numpy.ndarray
        3D mask volume

    zeroe: bool
        If true will remove the null timeseries voxels.  Only applied to timeseries (4D) data.

    Returns
    -------
    values: np.array
        An array of the values in the indicated ROI.
        A 2D matrix if `datavol` is 4D or a 1D vector if `datavol` is 3D.
    """
    if maskvol is not None:
        # get all masked time series within this roi r
        indices = (roivol == roivalue) * (maskvol > 0)
    else:
        # get all time series within this roi r
        indices = roivol == roivalue

    if datavol.ndim == 4:
        ts = datavol[indices, :]
    else:
        ts = datavol[indices]

    # remove zeroed time series
    if zeroe:
        if datavol.ndim == 4:
            ts = ts[ts.sum(axis=1) != 0, :]

    return ts