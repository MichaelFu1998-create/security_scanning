def _build_specs(self, specs, kwargs, fp_precision):
        """
        Returns the specs, the remaining kwargs and whether or not the
        constructor was called with kwarg or explicit specs.
        """
        if specs is None:
            overrides = param.ParamOverrides(self, kwargs,
                                             allow_extra_keywords=True)
            extra_kwargs = overrides.extra_keywords()
            kwargs = dict([(k,v) for (k,v) in kwargs.items()
                           if k not in extra_kwargs])
            rounded_specs = list(self.round_floats([extra_kwargs],
                                                   fp_precision))

            if extra_kwargs=={}: return [], kwargs, True
            else:                return rounded_specs, kwargs, False

        return list(self.round_floats(specs, fp_precision)), kwargs, True