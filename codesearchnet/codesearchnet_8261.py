def wait_for_and_get_block(self, block_number, blocks_waiting_for=None):
        """ Get the desired block from the chain, if the current head block is
            smaller (for both head and irreversible) then we wait, but a
            maxmimum of blocks_waiting_for * max_block_wait_repetition time
            before failure.

            :param int block_number: desired block number
            :param int blocks_waiting_for: (default) difference between
                block_number and current head how many blocks we are willing to
                wait, positive int
        """
        if not blocks_waiting_for:
            blocks_waiting_for = max(1, block_number - self.get_current_block_num())

        repetition = 0
        # can't return the block before the chain has reached it (support
        # future block_num)
        while self.get_current_block_num() < block_number:
            repetition += 1
            time.sleep(self.block_interval)
            if repetition > blocks_waiting_for * self.max_block_wait_repetition:
                raise Exception("Wait time for new block exceeded, aborting")
        # block has to be returned properly
        block = self.blockchain.rpc.get_block(block_number)
        repetition = 0
        while not block:
            repetition += 1
            time.sleep(self.block_interval)
            if repetition > self.max_block_wait_repetition:
                raise Exception("Wait time for new block exceeded, aborting")
            block = self.blockchain.rpc.get_block(block_number)
        return block