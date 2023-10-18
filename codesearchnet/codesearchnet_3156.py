def invoke(self, model, prefix_args=None):
        """
        Invoke a callable `model` as if it was a native function. If
        :func:`~manticore.models.isvariadic` returns true for `model`, `model` receives a single
        argument that is a generator for function arguments. Pass a tuple of
        arguments for `prefix_args` you'd like to precede the actual
        arguments.

        :param callable model: Python model of the function
        :param tuple prefix_args: Parameters to pass to model before actual ones
        :return: The result of calling `model`
        """
        prefix_args = prefix_args or ()

        arguments = self.get_argument_values(model, prefix_args)

        try:
            result = model(*arguments)
        except ConcretizeArgument as e:
            assert e.argnum >= len(prefix_args), "Can't concretize a constant arg"
            idx = e.argnum - len(prefix_args)

            # Arguments were lazily computed in case of variadic, so recompute here
            descriptors = self.get_arguments()
            src = next(islice(descriptors, idx, idx + 1))

            msg = 'Concretizing due to model invocation'
            if isinstance(src, str):
                raise ConcretizeRegister(self._cpu, src, msg)
            else:
                raise ConcretizeMemory(self._cpu.memory, src, self._cpu.address_bit_size, msg)
        else:
            if result is not None:
                self.write_result(result)

            self.ret()

        return result