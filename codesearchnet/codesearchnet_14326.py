def _extend_breaks(self, major):
        """
        Append 2 extra breaks at either end of major

        If breaks of transform space are non-equidistant,
        :func:`minor_breaks` add minor breaks beyond the first
        and last major breaks. The solutions is to extend those
        breaks (in transformed space) before the minor break call
        is made. How the breaks depends on the type of transform.
        """
        trans = self.trans
        trans = trans if isinstance(trans, type) else trans.__class__
        # so far we are only certain about this extending stuff
        # making sense for log transform
        is_log = trans.__name__.startswith('log')
        diff = np.diff(major)
        step = diff[0]
        if is_log and all(diff == step):
            major = np.hstack([major[0]-step, major, major[-1]+step])
        return major