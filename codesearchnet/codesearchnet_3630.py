def LDRD(cpu, dest1, dest2, src, offset=None):
        """Loads double width data from memory."""
        assert dest1.type == 'register'
        assert dest2.type == 'register'
        assert src.type == 'memory'
        mem1 = cpu.read_int(src.address(), 32)
        mem2 = cpu.read_int(src.address() + 4, 32)
        writeback = cpu._compute_writeback(src, offset)
        dest1.write(mem1)
        dest2.write(mem2)
        cpu._cs_hack_ldr_str_writeback(src, offset, writeback)