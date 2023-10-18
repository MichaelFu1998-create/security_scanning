def int80(self, cpu):
        """
        32 bit dispatcher.
        :param cpu: current CPU.
        _terminate, transmit, receive, fdwait, allocate, deallocate and random
        """
        syscalls = {0x00000001: self.sys_terminate,
                    0x00000002: self.sys_transmit,
                    0x00000003: self.sys_receive,
                    0x00000004: self.sys_fdwait,
                    0x00000005: self.sys_allocate,
                    0x00000006: self.sys_deallocate,
                    0x00000007: self.sys_random,
                    }
        if cpu.EAX not in syscalls.keys():
            raise TerminateState(f"32 bit DECREE system call number {cpu.EAX} Not Implemented")
        func = syscalls[cpu.EAX]
        logger.debug("SYSCALL32: %s (nargs: %d)", func.__name__, func.__code__.co_argcount)
        nargs = func.__code__.co_argcount
        args = [cpu, cpu.EBX, cpu.ECX, cpu.EDX, cpu.ESI, cpu.EDI, cpu.EBP]
        cpu.EAX = func(*args[:nargs - 1])