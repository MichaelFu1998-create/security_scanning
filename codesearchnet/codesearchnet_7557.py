def spectrum_data(filename):
    """Simple utilities to retrieve data sets from """
    import os
    import pkg_resources
    info = pkg_resources.get_distribution('spectrum')
    location = info.location

    # first try develop mode
    share = os.sep.join([location, "spectrum", 'data'])
    filename2 = os.sep.join([share, filename])
    if os.path.exists(filename2):
        return filename2
    else:
        raise Exception('unknown file %s' % filename2)