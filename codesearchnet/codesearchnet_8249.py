def whitelist(self, account):  # pragma: no cover
        """ Add an other account to the whitelist of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=["white"], account=self)