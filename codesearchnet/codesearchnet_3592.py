def SHA3(self, start, size):
        """Compute Keccak-256 hash"""
        # read memory from start to end
        # http://gavwood.com/paper.pdf
        data = self.try_simplify_to_constant(self.read_buffer(start, size))

        if issymbolic(data):
            known_sha3 = {}
            # Broadcast the signal
            self._publish('on_symbolic_sha3', data, known_sha3)  # This updates the local copy of sha3 with the pairs we need to explore

            value = 0  # never used
            known_hashes_cond = False
            for key, hsh in known_sha3.items():
                assert not issymbolic(key), "Saved sha3 data,hash pairs should be concrete"
                cond = key == data
                known_hashes_cond = Operators.OR(cond, known_hashes_cond)
                value = Operators.ITEBV(256, cond, hsh, value)
            return value

        value = sha3.keccak_256(data).hexdigest()
        value = int(value, 16)
        self._publish('on_concrete_sha3', data, value)
        logger.info("Found a concrete SHA3 example %r -> %x", data, value)
        return value