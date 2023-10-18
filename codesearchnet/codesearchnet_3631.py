def STRD(cpu, src1, src2, dest, offset=None):
        """Writes the contents of two registers to memory."""
        assert src1.type == 'register'
        assert src2.type == 'register'
        assert dest.type == 'memory'
        val1 = src1.read()
        val2 = src2.read()
        writeback = cpu._compute_writeback(dest, offset)
        cpu.write_int(dest.address(), val1, 32)
        cpu.write_int(dest.address() + 4, val2, 32)
        cpu._cs_hack_ldr_str_writeback(dest, offset, writeback)