def _rc_mget(self, keys, *args):
        """
        Returns a list of values ordered identically to ``*args``
        """
        args = list_or_args(keys, args)
        result = []
        for key in args:
            result.append(self.get(key))
        return result