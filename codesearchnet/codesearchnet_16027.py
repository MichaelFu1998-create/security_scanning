def to_bytes(self, previous: bytes):
        """
        Complex code ahead. Comments have been added in as needed.
        """
        # First, validate the lengths.
        if len(self.conditions) != len(self.body):
            raise exc.CompileError("Conditions and body length mismatch!")

        bc = b""

        prev_len = len(previous)

        # Loop over the conditions and bodies
        for condition, body in zip(self.conditions, self.body):
            # Generate the conditional data.
            cond_bytecode = condition.to_bytecode(previous)
            bc += cond_bytecode
            # Complex calculation. First, generate the bytecode for all tokens in the body. Then
            # we calculate the len() of that. We create a POP_JUMP_IF_FALSE operation that jumps
            # to the instructions after the body code + 3 for the pop call. This is done for all
            # chained IF calls, as if it was an elif call. Else calls are not possible to be
            # auto-generated, but it is possible to emulate them using an elif call that checks
            # for the opposite of the above IF.

            # Call the _compile_func method from compiler to compile the body.
            body_bc = compiler.compile_bytecode(body)

            bdyl = len(body_bc)
            # Add together the lengths.
            gen_len = prev_len + len(cond_bytecode) + bdyl + 1
            # Generate the POP_JUMP_IF_FALSE instruction
            bc += generate_simple_call(tokens.POP_JUMP_IF_FALSE, gen_len)
            # Add the body_bc
            bc += body_bc

            # Update previous_len
            prev_len = len(previous) + len(bc)

        return bc