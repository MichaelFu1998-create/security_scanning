def add_hook(self, pc, callback):
        """
        Add a callback to be invoked on executing a program counter. Pass `None`
        for pc to invoke callback on every instruction. `callback` should be a callable
        that takes one :class:`~manticore.core.state.State` argument.

        :param pc: Address of instruction to hook
        :type pc: int or None
        :param callable callback: Hook function
        """
        if not (isinstance(pc, int) or pc is None):
            raise TypeError(f"pc must be either an int or None, not {pc.__class__.__name__}")
        else:
            self._hooks.setdefault(pc, set()).add(callback)
            if self._hooks:
                self._executor.subscribe('will_execute_instruction', self._hook_callback)