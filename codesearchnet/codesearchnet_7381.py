def ss_wrap(func):
    """ ensure that a SavedSearch object exists """

    def wrapper(self, *args, **kwargs):
        if not self.savedsearch:
            self.savedsearch = SavedSearch(self)
        return func(self, *args, **kwargs)

    return wrapper