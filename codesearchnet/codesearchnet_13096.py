def memoize(func):
    """ Memoization decorator for a function taking one or more arguments. """
    class Memodict(dict):
        """ just a dict"""
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            """ this makes it faster """
            ret = self[key] = func(*key)
            return ret

    return Memodict().__getitem__