def refresh(self):
        """ Refresh/Obtain an account's data from the API server
        """
        import re

        if re.match(r"^1\.2\.[0-9]*$", self.identifier):
            account = self.blockchain.rpc.get_objects([self.identifier])[0]
        else:
            account = self.blockchain.rpc.lookup_account_names([self.identifier])[0]
        if not account:
            raise AccountDoesNotExistsException(self.identifier)
        self.store(account, "name")

        if self.full:  # pragma: no cover
            accounts = self.blockchain.rpc.get_full_accounts([account["id"]], False)
            if accounts and isinstance(accounts, list):
                account = accounts[0][1]
            else:
                raise AccountDoesNotExistsException(self.identifier)
            super(Account, self).__init__(
                account["account"], blockchain_instance=self.blockchain
            )
            for k, v in account.items():
                if k != "account":
                    self[k] = v
        else:
            super(Account, self).__init__(account, blockchain_instance=self.blockchain)