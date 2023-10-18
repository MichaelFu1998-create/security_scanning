def _setPath(cls):
    """ Sets the path of the custom configuration file
    """
    cls._path = os.path.join(os.environ['NTA_DYNAMIC_CONF_DIR'],
                             cls.customFileName)