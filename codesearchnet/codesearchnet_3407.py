def init(self, f):
        """
        A decorator used to register a hook function to run before analysis begins. Hook
        function takes one :class:`~manticore.core.state.State` argument.
        """
        def callback(manticore_obj, state):
            f(state)
        self.subscribe('will_start_run', types.MethodType(callback, self))
        return f