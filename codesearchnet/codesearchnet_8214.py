def convert_mode(image, mode='RGB'):
    """Return an image in the given mode."""
    deprecated.deprecated('util.gif.convert_model')

    return image if (image.mode == mode) else image.convert(mode=mode)