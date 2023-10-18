def to_bytes_35(self, previous: bytes):
        """
        A to-bytes specific to Python 3.5 and below.
        """

        # Calculations ahead.
        bc = b""

        # Calculate the length of the iterator.
        it_bc = util.generate_bytecode_from_obb(self.iterator, previous)
        bc += it_bc

        # Push a get_iter on.
        bc += util.generate_bytecode_from_obb(tokens.GET_ITER, b"")
        prev_len = len(previous) + len(bc)
        # Calculate the bytecode for the body.
        body_bc = b""
        for op in self._body:
            # Add padding bytes to the bytecode to allow if blocks to work.
            padded_bc = previous
            # Add padding for SETUP_LOOP
            padded_bc += b"\x00\x00\x00"
            padded_bc += bc
            # Add padding for FOR_ITER
            padded_bc += b"\x00\x00\x00"
            # Add previous body
            padded_bc += body_bc
            body_bc += util.generate_bytecode_from_obb(op, padded_bc)

        # Add a JUMP_ABSOLUTE
        body_bc += util.generate_simple_call(tokens.JUMP_ABSOLUTE, prev_len + 3)

        # Add a POP_TOP
        body_bc += util.generate_bytecode_from_obb(tokens.POP_BLOCK, b"")

        # Calculate the right lengths.
        # Add a FOR_ITER, using len(body_bc)
        body_bc = util.generate_simple_call(tokens.FOR_ITER, len(body_bc) - 1) + body_bc
        # Add the SETUP_LOOP call
        bc = util.generate_simple_call(tokens.SETUP_LOOP, prev_len + len(body_bc) - 6) + bc + body_bc

        return bc