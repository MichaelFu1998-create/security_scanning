def _PUNPCKL(cpu, dest, src, item_size):
        """
        Generic PUNPCKL
        """
        assert dest.size == src.size
        size = dest.size
        dest_value = dest.read()
        src_value = src.read()
        mask = (1 << item_size) - 1
        res = 0
        count = 0
        for pos in range(0, size // item_size):
            if count >= size:
                break
            item0 = Operators.ZEXTEND((dest_value >> (pos * item_size)) & mask, size)
            item1 = Operators.ZEXTEND((src_value >> (pos * item_size)) & mask, size)
            res |= item0 << count
            count += item_size
            res |= item1 << count
            count += item_size

        dest.write(res)