def add_jump(self, name, min, max, num, warp=None, var_type=float):
        """ An integer/float-valued enumerable with `num` items, bounded
        between [`min`, `max`]. Note that the right endpoint of the interval
        includes `max`. This is a wrapper around the add_enum. `jump` can be
        a float or int.
        """
        if not isinstance(var_type, type):
            if var_type == 'int':
                var_type = int
            elif var_type == 'float':
                var_type = float
            else:
                raise ValueError('var_type (%s) is not supported. use '
                                 '"int" or "float",' % (var_type))

        min, max = map(var_type, (min, max))
        num = int(num)

        if not warp:
            choices = np.linspace(min, max, num=num, dtype=var_type)
        elif (min >= 0) and warp == 'log':
            choices = np.logspace(np.log10(min), np.log10(max), num=num,
                                  dtype=var_type)
        elif (min <= 0)and warp == 'log':
            raise ValueError('variable %s: log-warping requires min > 0')
        else:
            raise ValueError('variable %s: warp=%s is not supported. use '
                             'None or "log",' % (name, warp))

        self.variables[name] = EnumVariable(name, choices.tolist())