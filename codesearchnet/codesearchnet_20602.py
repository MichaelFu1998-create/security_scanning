def get_rois_centers_of_mass(vol):
    """Get the center of mass for each ROI in the given volume.

    Parameters
    ----------
    vol: numpy ndarray
        Volume with different values for each ROI.

    Returns
    -------
    OrderedDict
        Each entry in the dict has the ROI value as key and the center_of_mass coordinate as value.
    """
    from scipy.ndimage.measurements import center_of_mass

    roisvals = np.unique(vol)
    roisvals = roisvals[roisvals != 0]

    rois_centers = OrderedDict()
    for r in roisvals:
        rois_centers[r] = center_of_mass(vol, vol, r)

    return rois_centers