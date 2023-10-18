def from_spec(spec, kwargs=None):
        """
        Creates a distribution from a specification dict.
        """
        distribution = util.get_object(
            obj=spec,
            predefined_objects=tensorforce.core.distributions.distributions,
            kwargs=kwargs
        )
        assert isinstance(distribution, Distribution)
        return distribution