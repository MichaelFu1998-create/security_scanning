def InColorspace(to_colorspace, from_colorspace="RGB", children=None, name=None, deterministic=False,
                 random_state=None):
    """Convert images to another colorspace."""
    return WithColorspace(to_colorspace, from_colorspace, children, name, deterministic, random_state)