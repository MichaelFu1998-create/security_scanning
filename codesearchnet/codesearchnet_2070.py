def from_spec(spec, kwargs=None):
        """
        Creates a baseline from a specification dict.
        """
        baseline = util.get_object(
            obj=spec,
            predefined_objects=tensorforce.core.baselines.baselines,
            kwargs=kwargs
        )
        assert isinstance(baseline, Baseline)
        return baseline