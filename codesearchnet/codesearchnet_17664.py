def _get_default_data_path_():
    """
    Calculate the default path in which thermochemical data is stored.

    :returns: Default path.
    """

    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r'data/rao')
    data_path = os.path.abspath(data_path)
    return data_path