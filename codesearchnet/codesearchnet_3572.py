def _get_memfee(self, address, size=1):
        """
        This calculates the amount of extra gas needed for accessing to
        previously unused memory.

        :param address: base memory offset
        :param size: size of the memory access
        """
        if not issymbolic(size) and size == 0:
            return 0

        address = self.safe_add(address, size)
        allocated = self.allocated
        GMEMORY = 3
        GQUADRATICMEMDENOM = 512  # 1 gas per 512 quadwords
        old_size = Operators.ZEXTEND(Operators.UDIV(self.safe_add(allocated, 31), 32), 512)
        new_size = Operators.ZEXTEND(Operators.UDIV(self.safe_add(address, 31), 32), 512)

        old_totalfee = self.safe_mul(old_size, GMEMORY) + Operators.UDIV(self.safe_mul(old_size, old_size), GQUADRATICMEMDENOM)
        new_totalfee = self.safe_mul(new_size, GMEMORY) + Operators.UDIV(self.safe_mul(new_size, new_size), GQUADRATICMEMDENOM)
        memfee = new_totalfee - old_totalfee
        flag = Operators.UGT(new_totalfee, old_totalfee)
        return Operators.ITEBV(512, size == 0, 0, Operators.ITEBV(512, flag, memfee, 0))