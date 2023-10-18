def clip_bounds(bounds=None, clip=None):
    """
    Clips bounds by clip.

    Parameters
    ----------
    bounds : bounds to be clipped
    clip : clip bounds

    Returns
    -------
    Bounds(left, bottom, right, top)
    """
    bounds = Bounds(*bounds)
    clip = Bounds(*clip)
    return Bounds(
        max(bounds.left, clip.left),
        max(bounds.bottom, clip.bottom),
        min(bounds.right, clip.right),
        min(bounds.top, clip.top)
    )