def sys_transmit(self, cpu, fd, buf, count, tx_bytes):
        """
        Symbolic version of Decree.sys_transmit
        """
        if issymbolic(fd):
            logger.info("Ask to write to a symbolic file descriptor!!")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 0)

        if issymbolic(buf):
            logger.info("Ask to write to a symbolic buffer")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 1)

        if issymbolic(count):
            logger.info("Ask to write a symbolic number of bytes ")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 2)

        if issymbolic(tx_bytes):
            logger.info("Ask to return size to a symbolic address ")
            cpu.PC = cpu.PC - cpu.instruction.size
            raise SymbolicSyscallArgument(cpu, 3)

        return super().sys_transmit(cpu, fd, buf, count, tx_bytes)