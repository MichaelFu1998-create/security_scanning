def _read_string(self, cpu, buf):
        """
        Reads a null terminated concrete buffer form memory
        :todo: FIX. move to cpu or memory
        """
        filename = ""
        for i in range(0, 1024):
            c = Operators.CHR(cpu.read_int(buf + i, 8))
            if c == '\x00':
                break
            filename += c
        return filename