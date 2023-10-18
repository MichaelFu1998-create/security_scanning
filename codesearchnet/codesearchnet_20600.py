def create_rois_mask(roislist, filelist):
    """Look for the files in filelist containing the names in roislist, these files will be opened, binarised
    and merged in one mask.

    Parameters
    ----------
    roislist: list of strings
        Names of the ROIs, which will have to be in the names of the files in filelist.

    filelist: list of strings
        List of paths to the volume files containing the ROIs.

    Returns
    -------
    numpy.ndarray
        Mask volume
    """
    roifiles = []

    for roi in roislist:
        try:
            roi_file = search_list(roi, filelist)[0]
        except Exception as exc:
            raise Exception('Error creating list of roi files. \n {}'.format(str(exc)))
        else:
            roifiles.append(roi_file)

    return binarise(roifiles)