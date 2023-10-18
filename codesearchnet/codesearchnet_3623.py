def _write_APSR(self, apsr):
        """Auxiliary function - Writes flags from a full APSR (only 4 msb used)"""
        V = Operators.EXTRACT(apsr, 28, 1)
        C = Operators.EXTRACT(apsr, 29, 1)
        Z = Operators.EXTRACT(apsr, 30, 1)
        N = Operators.EXTRACT(apsr, 31, 1)

        self.write('APSR_V', V)
        self.write('APSR_C', C)
        self.write('APSR_Z', Z)
        self.write('APSR_N', N)