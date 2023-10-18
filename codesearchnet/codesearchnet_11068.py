def parse_package_string(path):
    """
    Parse the effect package string.
    Can contain the package python path or path to effect class in an effect package.

    Examples::

        # Path to effect pacakge
        examples.cubes

        # Path to effect class
        examples.cubes.Cubes

    Args:
        path: python path to effect package. May also include effect class name.

    Returns:
        tuple: (package_path, effect_class)
    """
    parts = path.split('.')

    # Is the last entry in the path capitalized?
    if parts[-1][0].isupper():
        return ".".join(parts[:-1]), parts[-1]

    return path, ""