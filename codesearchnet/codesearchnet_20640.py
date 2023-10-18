def get_nifti1hdr_from_h5attrs(h5attrs):
    """Transforms an H5py Attributes set to a dict.
    Converts unicode string keys into standard strings
    and each value into a numpy array.

    Parameters
    ----------
    h5attrs: H5py Attributes

    Returns
    --------
    dict
    """
    hdr = nib.Nifti1Header()
    for k in list(h5attrs.keys()):
        hdr[str(k)] = np.array(h5attrs[k])

    return hdr