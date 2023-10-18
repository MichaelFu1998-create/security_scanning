def block_hash(self, block_number=None, force_recent=True):
        """
        Calculates a block's hash
        :param block_number: the block number for which to calculate the hash, defaulting to the most recent block
        :param force_recent: if True (the default) return zero for any block that is in the future or older than 256 blocks
        :return: the block hash
        """
        if block_number is None:
            block_number = self.block_number() - 1

        # We are not maintaining an actual -block-chain- so we just generate
        # some hashes for each virtual block
        value = sha3.keccak_256((repr(block_number) + 'NONCE').encode()).hexdigest()
        value = int(value, 16)

        if force_recent:
            # 0 is left on the stack if the looked for block number is greater or equal
            # than the current block number or more than 256 blocks behind the current
            # block. (Current block hash is unknown from inside the tx)
            bnmax = Operators.ITEBV(256, self.block_number() > 256, 256, self.block_number())
            value = Operators.ITEBV(256, Operators.OR(block_number >= self.block_number(), block_number < bnmax), 0, value)

        return value