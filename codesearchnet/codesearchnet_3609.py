def human_transactions(self):
        """Completed human transaction"""
        txs = []
        for tx in self.transactions:
            if tx.depth == 0:
                txs.append(tx)
        return tuple(txs)