def sys_receive(self, cpu, fd, buf, count, rx_bytes):
        """
        Symbolic version of Decree.sys_receive
        """
        if issymbolic(fd):
            logger.info("Ask to read from a symbolic file descriptor!!")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 0)

        if issymbolic(buf):
            logger.info("Ask to read to a symbolic buffer")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 1)

        if issymbolic(count):
            logger.info("Ask to read a symbolic number of bytes ")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 2)

        if issymbolic(rx_bytes):
            logger.info("Ask to return size to a symbolic address ")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 3)

        return super().sys_receive(cpu, fd, buf, count, rx_bytes)