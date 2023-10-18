def get_argument_values(self, model, prefix_args):
        """
        Extract arguments for model from the environment and return as a tuple that
        is ready to be passed to the model.

        :param callable model: Python model of the function
        :param tuple prefix_args: Parameters to pass to model before actual ones
        :return: Arguments to be passed to the model
        :rtype: tuple
        """
        spec = inspect.getfullargspec(model)

        if spec.varargs:
            logger.warning("ABI: A vararg model must be a unary function.")

        nargs = len(spec.args) - len(prefix_args)

        # If the model is a method, we need to account for `self`
        if inspect.ismethod(model):
            nargs -= 1

        def resolve_argument(arg):
            if isinstance(arg, str):
                return self._cpu.read_register(arg)
            else:
                return self._cpu.read_int(arg)

        # Create a stream of resolved arguments from argument descriptors
        descriptors = self.get_arguments()
        argument_iter = map(resolve_argument, descriptors)

        from ..models import isvariadic  # prevent circular imports

        if isvariadic(model):
            arguments = prefix_args + (argument_iter,)
        else:
            arguments = prefix_args + tuple(islice(argument_iter, nargs))

        return arguments