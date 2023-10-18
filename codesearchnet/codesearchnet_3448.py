def write_back_memory(self, where, expr, size):
        """ Copy memory writes from Manticore back into Unicorn in real-time """
        if self.write_backs_disabled:
            return
        if type(expr) is bytes:
            self._emu.mem_write(where, expr)
        else:
            if issymbolic(expr):
                data = [Operators.CHR(Operators.EXTRACT(expr, offset, 8)) for offset in range(0, size, 8)]
                concrete_data = []
                for c in data:
                    if issymbolic(c):
                        c = chr(solver.get_value(self._cpu.memory.constraints, c))
                    concrete_data.append(c)
                data = concrete_data
            else:
                data = [Operators.CHR(Operators.EXTRACT(expr, offset, 8)) for offset in range(0, size, 8)]
            logger.debug(f"Writing back {hr_size(size // 8)} to {hex(where)}: {data}")
            # TODO - the extra encoding is to handle null bytes output as strings when we concretize. That's probably a bug.
            self._emu.mem_write(where, b''.join(b.encode('utf-8') if type(b) is str else b for b in data))