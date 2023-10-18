def appendSigner(self, accounts, permission):
        """ Try to obtain the wif key from the wallet by telling which account
            and permission is supposed to sign the transaction
        """
        assert permission in self.permission_types, "Invalid permission"

        if self.blockchain.wallet.locked():
            raise WalletLocked()
        if not isinstance(accounts, (list, tuple, set)):
            accounts = [accounts]

        for account in accounts:
            # Now let's actually deal with the accounts
            if account not in self.signing_accounts:
                # is the account an instance of public key?
                if isinstance(account, self.publickey_class):
                    self.appendWif(
                        self.blockchain.wallet.getPrivateKeyForPublicKey(str(account))
                    )
                # ... or should we rather obtain the keys from an account name
                else:
                    accountObj = self.account_class(
                        account, blockchain_instance=self.blockchain
                    )
                    required_treshold = accountObj[permission]["weight_threshold"]
                    keys = self._fetchkeys(
                        accountObj, permission, required_treshold=required_treshold
                    )
                    # If we couldn't find an active key, let's try overwrite it
                    # with an owner key
                    if not keys and permission != "owner":
                        keys.extend(
                            self._fetchkeys(
                                accountObj, "owner", required_treshold=required_treshold
                            )
                        )
                    for x in keys:
                        self.appendWif(x[0])

                self.signing_accounts.append(account)