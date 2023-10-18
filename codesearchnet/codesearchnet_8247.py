def history(self, first=0, last=0, limit=-1, only_ops=[], exclude_ops=[]):
        """ Returns a generator for individual account transactions. The
            latest operation will be first. This call can be used in a
            ``for`` loop.

            :param int first: sequence number of the first
                transaction to return (*optional*)
            :param int last: sequence number of the last
                transaction to return (*optional*)
            :param int limit: limit number of transactions to
                return (*optional*)
            :param array only_ops: Limit generator by these
                operations (*optional*)
            :param array exclude_ops: Exclude these operations from
                generator (*optional*).

            ... note::
                only_ops and exclude_ops takes an array of strings:
                The full list of operation ID's can be found in
                operationids.py.
                Example: ['transfer', 'fill_order']
        """
        _limit = 100
        cnt = 0

        if first < 0:
            first = 0

        while True:
            # RPC call
            txs = self.blockchain.rpc.get_account_history(
                self["id"],
                "1.11.{}".format(last),
                _limit,
                "1.11.{}".format(first - 1),
                api="history",
            )
            for i in txs:
                if (
                    exclude_ops
                    and self.operations.getOperationNameForId(i["op"][0]) in exclude_ops
                ):
                    continue
                if (
                    not only_ops
                    or self.operations.getOperationNameForId(i["op"][0]) in only_ops
                ):
                    cnt += 1
                    yield i
                    if limit >= 0 and cnt >= limit:  # pragma: no cover
                        return

            if not txs:
                log.info("No more history returned from API node")
                break
            if len(txs) < _limit:
                log.info("Less than {} have been returned.".format(_limit))
                break
            first = int(txs[-1]["id"].split(".")[2])