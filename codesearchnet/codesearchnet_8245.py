def balances(self):
        """ List balances of an account. This call returns instances of
            :class:`amount.Amount`.
        """
        balances = self.blockchain.rpc.get_account_balances(self["id"], [])
        return [
            self.amount_class(b, blockchain_instance=self.blockchain)
            for b in balances
            if int(b["amount"]) > 0
        ]