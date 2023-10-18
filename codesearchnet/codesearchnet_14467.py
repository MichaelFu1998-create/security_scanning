def add_int(self, name, min, max, warp=None):
        """An integer-valued dimension bounded between `min` <= x <= `max`.
        Note that the right endpoint of the interval includes `max`.

        When `warp` is None, the base measure associated with this dimension
        is a categorical distribution with each weight on each of the integers
        in [min, max]. With `warp == 'log'`, the base measure is a uniform
        distribution on the log of the variable, with bounds at `log(min)` and
        `log(max)`. This is appropriate for variables that are "naturally" in
        log-space. Other `warp` functions are not supported (yet), but may be
        at a later time. Please note that this functionality is not supported
        for `hyperopt_tpe`.
        """
        min, max = map(int, (min, max))
        if max < min:
            raise ValueError('variable %s: max < min error' % name)
        if warp not in (None, 'log'):
            raise ValueError('variable %s: warp=%s is not supported. use '
                             'None or "log",' % (name, warp))
        if min <= 0 and warp == 'log':
            raise ValueError('variable %s: log-warping requires min > 0')

        self.variables[name] = IntVariable(name, min, max, warp)