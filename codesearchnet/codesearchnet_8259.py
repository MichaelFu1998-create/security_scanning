def block_timestamp(self, block_num):
        """ Returns the timestamp of the block with the given block
            number.

            :param int block_num: Block number
        """
        return int(
            self.block_class(block_num, blockchain_instance=self.blockchain)
            .time()
            .timestamp()
        )