def addSigningInformation(self, account, permission):
        """ This is a private method that adds side information to a
            unsigned/partial transaction in order to simplify later
            signing (e.g. for multisig or coldstorage)

            FIXME: Does not work with owner keys!
        """
        self.constructTx()
        self["blockchain"] = self.blockchain.rpc.chain_params

        if isinstance(account, self.publickey_class):
            self["missing_signatures"] = [str(account)]
        else:
            accountObj = self.account_class(account)
            authority = accountObj[permission]
            # We add a required_authorities to be able to identify
            # how to sign later. This is an array, because we
            # may later want to allow multiple operations per tx
            self.update({"required_authorities": {accountObj["name"]: authority}})
            for account_auth in authority["account_auths"]:
                account_auth_account = self.account_class(account_auth[0])
                self["required_authorities"].update(
                    {account_auth[0]: account_auth_account.get(permission)}
                )

            # Try to resolve required signatures for offline signing
            self["missing_signatures"] = [x[0] for x in authority["key_auths"]]
            # Add one recursion of keys from account_auths:
            for account_auth in authority["account_auths"]:
                account_auth_account = self.account_class(account_auth[0])
                self["missing_signatures"].extend(
                    [x[0] for x in account_auth_account[permission]["key_auths"]]
                )