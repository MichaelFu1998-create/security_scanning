def scale_in(self, blocks=None, block_ids=[]):
        """Scale in the number of active blocks by specified amount.

        The scale in method here is very rude. It doesn't give the workers
        the opportunity to finish current tasks or cleanup. This is tracked
        in issue #530

        Parameters
        ----------

        blocks : int
             Number of blocks to terminate and scale_in by

        block_ids : list
             List of specific block ids to terminate. Optional

        Raises:
             NotImplementedError
        """

        if block_ids:
            block_ids_to_kill = block_ids
        else:
            block_ids_to_kill = list(self.blocks.keys())[:blocks]

        # Hold the block
        for block_id in block_ids_to_kill:
            self._hold_block(block_id)

        # Now kill via provider
        to_kill = [self.blocks.pop(bid) for bid in block_ids_to_kill]

        if self.provider:
            r = self.provider.cancel(to_kill)

        return r