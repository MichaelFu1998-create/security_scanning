def _rc_sinterstore(self, dst, src, *args):
        """
        Store the difference of sets ``src``,  ``args`` into a new
        set named ``dest``.  Returns the number of keys in the new set.
        """
        args = list_or_args(src, args)
        result = self.sinter(*args)
        if result is not set([]):
            return self.sadd(dst, *list(result))
        return 0