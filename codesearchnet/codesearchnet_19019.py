def _rc_sunion(self, src, *args):
        """
        Returns the members of the set resulting from the union between
        the first set and all the successive sets.
        """
        args = list_or_args(src, args)
        src_set = self.smembers(args.pop(0))
        if src_set is not set([]):
            for key in args:
                src_set.update(self.smembers(key))
        return src_set