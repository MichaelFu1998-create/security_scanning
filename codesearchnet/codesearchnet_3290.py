def _getMemoryBit(cpu, bitbase, bitoffset):
        """ Calculate address and bit offset given a base address and a bit offset
            relative to that address (in the form of asm operands) """
        assert bitbase.type == 'memory'
        assert bitbase.size >= bitoffset.size
        addr = bitbase.address()
        offt = Operators.SEXTEND(bitoffset.read(), bitoffset.size, bitbase.size)
        offt_is_neg = offt >= (1 << (bitbase.size - 1))
        offt_in_bytes = offt // 8
        bitpos = offt % 8

        new_addr = addr + Operators.ITEBV(bitbase.size, offt_is_neg, -offt_in_bytes, offt_in_bytes)
        return (new_addr, bitpos)