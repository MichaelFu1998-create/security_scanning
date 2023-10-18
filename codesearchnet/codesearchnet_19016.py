def _rc_sinter(self, src, *args):
        """
        Returns the members of the set resulting from the difference between
        the first set and all the successive sets.
        """
        args = list_or_args(src, args)
        src_set = self.smembers(args.pop(0))
        if src_set is not set([]):
            for key in args:
                src_set.intersection_update(self.smembers(key))
        return src_set