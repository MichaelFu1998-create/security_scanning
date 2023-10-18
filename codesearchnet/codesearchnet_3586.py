def EXP_gas(self, base, exponent):
        """Calculate extra gas fee"""
        EXP_SUPPLEMENTAL_GAS = 10   # cost of EXP exponent per byte

        def nbytes(e):
            result = 0
            for i in range(32):
                result = Operators.ITEBV(512, Operators.EXTRACT(e, i * 8, 8) != 0, i + 1, result)
            return result
        return EXP_SUPPLEMENTAL_GAS * nbytes(exponent)