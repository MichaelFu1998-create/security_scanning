def nolist(self, account):  # pragma: no cover
        """ Remove an other account from any list of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=[], account=self)