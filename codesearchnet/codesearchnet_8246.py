def balance(self, symbol):
        """ Obtain the balance of a specific Asset. This call returns instances of
            :class:`amount.Amount`.
        """
        if isinstance(symbol, dict) and "symbol" in symbol:
            symbol = symbol["symbol"]
        balances = self.balances
        for b in balances:
            if b["symbol"] == symbol:
                return b
        return self.amount_class(0, symbol, blockchain_instance=self.blockchain)