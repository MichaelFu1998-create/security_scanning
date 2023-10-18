def blocks(self, start=None, stop=None):
        """ Yields blocks starting from ``start``.

            :param int start: Starting block
            :param int stop: Stop at this block
            :param str mode: We here have the choice between
             "head" (the last block) and "irreversible" (the block that is
             confirmed by 2/3 of all block producers and is thus irreversible)
        """
        # Let's find out how often blocks are generated!
        self.block_interval = self.get_block_interval()

        if not start:
            start = self.get_current_block_num()

        # We are going to loop indefinitely
        while True:

            # Get chain properies to identify the
            if stop:
                head_block = stop
            else:
                head_block = self.get_current_block_num()

            # Blocks from start until head block
            for blocknum in range(start, head_block + 1):
                # Get full block
                block = self.wait_for_and_get_block(blocknum)
                block.update({"block_num": blocknum})
                yield block
            # Set new start
            start = head_block + 1

            if stop and start > stop:
                # raise StopIteration
                return

            # Sleep for one block
            time.sleep(self.block_interval)