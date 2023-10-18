def ops(self, start=None, stop=None, **kwargs):
        """ Yields all operations (excluding virtual operations) starting from
            ``start``.

            :param int start: Starting block
            :param int stop: Stop at this block
            :param str mode: We here have the choice between
             "head" (the last block) and "irreversible" (the block that is
             confirmed by 2/3 of all block producers and is thus irreversible)
            :param bool only_virtual_ops: Only yield virtual operations

            This call returns a list that only carries one operation and
            its type!
        """

        for block in self.blocks(start=start, stop=stop, **kwargs):
            for tx in block["transactions"]:
                for op in tx["operations"]:
                    # Replace opid by op name
                    op[0] = self.operationids.getOperationName(op[0])
                    yield {
                        "block_num": block["block_num"],
                        "op": op,
                        "timestamp": block["timestamp"],
                    }