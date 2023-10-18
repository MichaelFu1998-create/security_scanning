def syscall(self):
        """
        Syscall dispatcher.
        """

        index = self._syscall_abi.syscall_number()

        try:
            table = getattr(linux_syscalls, self.current.machine)
            name = table.get(index, None)
            implementation = getattr(self, name)
        except (AttributeError, KeyError):
            if name is not None:
                raise SyscallNotImplemented(index, name)
            else:
                raise Exception(f"Bad syscall index, {index}")

        return self._syscall_abi.invoke(implementation)