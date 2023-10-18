def block_time(self, block_num):
        """ Returns a datetime of the block with the given block
            number.

            :param int block_num: Block number
        """
        return self.block_class(block_num, blockchain_instance=self.blockchain).time()