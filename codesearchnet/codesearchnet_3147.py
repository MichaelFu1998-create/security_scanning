def read(self, address, size, force=False):
        """
        Read a stream of potentially symbolic bytes from a potentially symbolic
        address

        :param address: Where to read from
        :param size: How many bytes
        :param force: Whether to ignore permissions
        :rtype: list
        """
        size = self._get_size(size)
        assert not issymbolic(size)

        if issymbolic(address):
            assert solver.check(self.constraints)
            logger.debug(f'Reading {size} bytes from symbolic address {address}')
            try:
                solutions = self._try_get_solutions(address, size, 'r', force=force)
                assert len(solutions) > 0
            except TooManySolutions as e:
                m, M = solver.minmax(self.constraints, address)
                logger.debug(f'Got TooManySolutions on a symbolic read. Range [{m:x}, {M:x}]. Not crashing!')

                # The force param shouldn't affect this, as this is checking for unmapped reads, not bad perms
                crashing_condition = True
                for start, end, perms, offset, name in self.mappings():
                    if start <= M + size and end >= m:
                        if 'r' in perms:
                            crashing_condition = Operators.AND(Operators.OR((address + size).ult(start), address.uge(end)), crashing_condition)

                if solver.can_be_true(self.constraints, crashing_condition):
                    raise InvalidSymbolicMemoryAccess(address, 'r', size, crashing_condition)

                # INCOMPLETE Result! We could also fork once for every map
                logger.info('INCOMPLETE Result! Using the sampled solutions we have as result')
                condition = False
                for base in e.solutions:
                    condition = Operators.OR(address == base, condition)
                from .state import ForkState
                raise ForkState("Forking state on incomplete result", condition)

            # So here we have all potential solutions to address

            condition = False
            for base in solutions:
                condition = Operators.OR(address == base, condition)

            result = []
            # consider size ==1 to read following code
            for offset in range(size):
                # Given ALL solutions for the symbolic address
                for base in solutions:
                    addr_value = base + offset
                    byte = Operators.ORD(self.map_containing(addr_value)[addr_value])
                    if addr_value in self._symbols:
                        for condition, value in self._symbols[addr_value]:
                            byte = Operators.ITEBV(8, condition, Operators.ORD(value), byte)
                    if len(result) > offset:
                        result[offset] = Operators.ITEBV(8, address == base, byte, result[offset])
                    else:
                        result.append(byte)
                    assert len(result) == offset + 1
            return list(map(Operators.CHR, result))
        else:
            result = list(map(Operators.ORD, super().read(address, size, force)))
            for offset in range(size):
                if address + offset in self._symbols:
                    for condition, value in self._symbols[address + offset]:
                        if condition is True:
                            result[offset] = Operators.ORD(value)
                        else:
                            result[offset] = Operators.ITEBV(8, condition, Operators.ORD(value), result[offset])
            return list(map(Operators.CHR, result))