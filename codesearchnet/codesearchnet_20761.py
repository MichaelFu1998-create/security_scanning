def copy_attributes(source, destination, ignore_patterns=[]):
    """
    Copy the attributes from a source object to a destination object.
    """
    for attr in _wildcard_filter(dir(source), *ignore_patterns):
        setattr(destination, attr, getattr(source, attr))