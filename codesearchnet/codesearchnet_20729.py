def remove_dcm2nii_underprocessed(filepaths):
    """ Return a subset of `filepaths`. Keep only the files that have a basename longer than the
    others with same suffix.
    This works based on that dcm2nii appends a preffix character for each processing
    step it does automatically in the DICOM to NifTI conversion.

    Parameters
    ----------
    filepaths: iterable of str

    Returns
    -------
    cleaned_paths: iterable of str
    """
    cln_flist = []

    # sort them by size
    len_sorted = sorted(filepaths, key=len)

    for idx, fpath in enumerate(len_sorted):
        remove = False

        # get the basename and the rest of the files
        fname = op.basename(fpath)
        rest  = len_sorted[idx+1:]

        # check if the basename is in the basename of the rest of the files
        for rest_fpath in rest:
            rest_file = op.basename(rest_fpath)
            if rest_file.endswith(fname):
                remove = True
                break

        if not remove:
            cln_flist.append(fpath)

    return cln_flist