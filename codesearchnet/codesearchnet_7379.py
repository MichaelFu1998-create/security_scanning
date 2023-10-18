def cleanwrap(func):
    """ Wrapper for Zotero._cleanup
    """

    def enc(self, *args, **kwargs):
        """ Send each item to _cleanup() """
        return (func(self, item, **kwargs) for item in args)

    return enc