def locked_context(self, key=None, value_type=list):
        """
        A context manager that provides safe parallel access to the global Manticore context.
        This should be used to access the global Manticore context
        when parallel analysis is activated. Code within the `with` block is executed
        atomically, so access of shared variables should occur within.
        """
        plugin_context_name = str(type(self))
        with self.manticore.locked_context(plugin_context_name, dict) as context:
            assert value_type in (list, dict, set)
            ctx = context.get(key, value_type())
            yield ctx
            context[key] = ctx