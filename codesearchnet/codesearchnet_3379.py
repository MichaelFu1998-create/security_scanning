def locked_context(self, key=None, value_type=list):
        """
        A context manager that provides safe parallel access to the global Manticore context.
        This should be used to access the global Manticore context
        when parallel analysis is activated. Code within the `with` block is executed
        atomically, so access of shared variables should occur within.

        Example use::

            with m.locked_context() as context:
                visited = context['visited']
                visited.append(state.cpu.PC)
                context['visited'] = visited

        Optionally, parameters can specify a key and type for the object paired to this key.::

            with m.locked_context('feature_list', list) as feature_list:
                feature_list.append(1)

        :param object key: Storage key
        :param value_type: type of value associated with key
        :type value_type: list or dict or set
        """

        @contextmanager
        def _real_context():
            if self._context is not None:
                yield self._context
            else:
                with self._executor.locked_context() as context:
                    yield context

        with _real_context() as context:
            if key is None:
                yield context
            else:
                assert value_type in (list, dict, set)
                ctx = context.get(key, value_type())
                yield ctx
                context[key] = ctx