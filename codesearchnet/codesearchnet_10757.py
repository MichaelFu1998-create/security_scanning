def set_default_sim_param(self, *args, **kwargs):
        """Set the simulation default simulation parameters.

        You can pass one of two things in as input:
        - a kappa_common.SimulationParameter instance
        - the arguments and keyword argument to create such an instance.

        The parameters you specify will be used by default in simulations run
        by this client.
        """
        if len(args) is 1 and isinstance(args[0], SimulationParameter):
            self.__default_param = args[0]
        else:
            self.__default_param = SimulationParameter(*args, **kwargs)
        return