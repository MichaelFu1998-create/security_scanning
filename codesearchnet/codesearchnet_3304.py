def PMINUB(cpu, dest, src):
        """
        PMINUB: returns minimum of packed unsigned byte integers in the dest operand
        see PMAXUB
        """
        dest_value = dest.read()
        src_value = src.read()
        result = 0
        for pos in range(0, dest.size, 8):
            itema = (dest_value >> pos) & 0xff
            itemb = (src_value >> pos) & 0xff
            result |= Operators.ITEBV(dest.size, itema < itemb, itema, itemb) << pos
        dest.write(result)