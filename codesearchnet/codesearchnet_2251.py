def from_config(config, kwargs=None):
        """
        Creates a solver from a specification dict.
        """
        return util.get_object(
            obj=config,
            predefined=tensorforce.core.optimizers.solvers.solvers,
            kwargs=kwargs
        )