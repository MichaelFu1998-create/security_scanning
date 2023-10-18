def blacklist(self, account):  # pragma: no cover
        """ Add an other account to the blacklist of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=["black"], account=self)