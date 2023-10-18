def hook(self, pc):
        """
        A decorator used to register a hook function for a given instruction address.
        Equivalent to calling :func:`~add_hook`.

        :param pc: Address of instruction to hook
        :type pc: int or None
        """
        def decorator(f):
            self.add_hook(pc, f)
            return f
        return decorator