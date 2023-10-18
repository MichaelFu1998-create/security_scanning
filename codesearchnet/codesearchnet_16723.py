def get_description():
    """Get long description from README."""
    with open(path.join(here, 'README.rst'), 'r') as f:
        data = f.read()
    return data