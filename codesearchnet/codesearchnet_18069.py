def sample(field, inds=None, slicer=None, flat=True):
    """
    Take a sample from a field given flat indices or a shaped slice

    Parameters
    -----------
    inds : list of indices
        One dimensional (raveled) indices to return from the field

    slicer : slice object
        A shaped (3D) slicer that returns a section of image

    flat : boolean
        Whether to flatten the sampled item before returning
    """
    if inds is not None:
        out = field.ravel()[inds]
    elif slicer is not None:
        out = field[slicer].ravel()
    else:
        out = field

    if flat:
        return out.ravel()
    return out