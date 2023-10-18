def read_yaml_file(path, loader=ExtendedSafeLoader):
    """Open a file, read it and return its contents."""
    with open(path) as fh:
        return load(fh, loader)