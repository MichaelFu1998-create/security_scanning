def process_keys(func):
    """
    Raise error for keys that are not strings
    and add the prefix if it is missing
    """

    @wraps(func)
    def decorated(self, k, *args):
        if not isinstance(k, str):
            msg = "%s: key must be a string" % self.__class__.__name__
            raise ValueError(msg)

        if not k.startswith(self.prefix):
            k = self.prefix + k

        return func(self, k, *args)

    return decorated