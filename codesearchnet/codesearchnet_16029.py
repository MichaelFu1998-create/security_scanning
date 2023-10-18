def to_bytes_36(self, previous: bytes):
        """
        A to-bytes specific to Python 3.6 and above.
        """
        # Calculations ahead.
        bc = b""

        # Calculate the length of the iterator.
        it_bc = util.generate_bytecode_from_obb(self.iterator, previous)
        bc += it_bc

        bc += util.ensure_instruction(tokens.GET_ITER)