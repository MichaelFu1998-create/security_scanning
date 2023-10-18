def values_from(self, base):
        """
        A reusable generator for increasing pointer-sized values from an address
        (usually the stack).
        """
        word_bytes = self._cpu.address_bit_size // 8
        while True:
            yield base
            base += word_bytes