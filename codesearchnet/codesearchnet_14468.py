def add_float(self, name, min, max, warp=None):
        """A floating point-valued dimension bounded `min` <= x < `max`

        When `warp` is None, the base measure associated with this dimension
        is a uniform distribution on [min, max). With `warp == 'log'`, the
        base measure is a uniform distribution on the log of the variable,
        with bounds at `log(min)` and `log(max)`. This is appropriate for
        variables that are "naturally" in log-space. Other `warp` functions
        are not supported (yet), but may be at a later time.
        """
        min, max = map(float, (min, max))
        if not min < max:
            raise ValueError('variable %s: min >= max error' % name)
        if warp not in (None, 'log'):
            raise ValueError('variable %s: warp=%s is not supported. use '
                             'None or "log",' % (name, warp))
        if min <= 0 and warp == 'log':
            raise ValueError('variable %s: log-warping requires min > 0')

        self.variables[name] = FloatVariable(name, min, max, warp)