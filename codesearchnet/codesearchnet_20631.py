def get_3D_from_4D(filename, vol_idx=0):
    """Return a 3D volume from a 4D nifti image file

    Parameters
    ----------
    filename: str
        Path to the 4D .mhd file

    vol_idx: int
        Index of the 3D volume to be extracted from the 4D volume.

    Returns
    -------
    vol, hdr
        The data array and the new 3D image header.
    """
    def remove_4th_element_from_hdr_string(hdr, fieldname):
        if fieldname in hdr:
            hdr[fieldname] = ' '.join(hdr[fieldname].split()[:3])

    vol, hdr = load_raw_data_with_mhd(filename)

    if vol.ndim != 4:
        raise ValueError('Volume in {} does not have 4 dimensions.'.format(op.join(op.dirname(filename),
                                                                                   hdr['ElementDataFile'])))

    if not 0 <= vol_idx < vol.shape[3]:
        raise IndexError('IndexError: 4th dimension in volume {} has {} volumes, not {}.'.format(filename,
                                                                                                 vol.shape[3], vol_idx))

    new_vol = vol[:, :, :, vol_idx].copy()

    hdr['NDims'] = 3
    remove_4th_element_from_hdr_string(hdr, 'ElementSpacing')
    remove_4th_element_from_hdr_string(hdr, 'DimSize')

    return new_vol, hdr