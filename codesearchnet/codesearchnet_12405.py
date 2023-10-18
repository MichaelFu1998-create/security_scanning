def refresh(self):
        """
        Reloads the wallet and its accounts. By default, this method is called only once,
        on :class:`Wallet` initialization. When the wallet is accessed by multiple clients or
        exists in multiple instances, calling `refresh()` will be necessary to update
        the list of accounts.
        """
        self.accounts = self.accounts or []
        idx = 0
        for _acc in self._backend.accounts():
            _acc.wallet = self
            try:
                if self.accounts[idx]:
                    continue
            except IndexError:
                pass
            self.accounts.append(_acc)
            idx += 1