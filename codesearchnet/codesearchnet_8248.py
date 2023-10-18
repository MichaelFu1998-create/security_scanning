def upgrade(self):  # pragma: no cover
        """ Upgrade account to life time member
        """
        assert callable(self.blockchain.upgrade_account)
        return self.blockchain.upgrade_account(account=self)