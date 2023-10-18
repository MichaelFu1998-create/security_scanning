def _os_name_factory(settings):
    """Factory for the :r:`software_os setting` default.
    """
    # pylint: disable-msg=W0613,W0142
    return u"{0} {1} {2}".format(platform.system(), platform.release(),
                                                        platform.machine())