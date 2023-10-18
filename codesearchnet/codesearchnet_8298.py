def claim(self, account=None, **kwargs):
        """ Claim a balance from the genesis block

            :param str balance_id: The identifier that identifies the balance
                to claim (1.15.x)
            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in self.blockchain.config:
                account = self.blockchain.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = self.account_class(account, blockchain_instance=self.blockchain)
        pubkeys = self.blockchain.wallet.getPublicKeys()
        addresses = dict()
        for p in pubkeys:
            if p[: len(self.blockchain.prefix)] != self.blockchain.prefix:
                continue
            pubkey = self.publickey_class(p, prefix=self.blockchain.prefix)
            addresses[
                str(
                    self.address_class.from_pubkey(
                        pubkey,
                        compressed=False,
                        version=0,
                        prefix=self.blockchain.prefix,
                    )
                )
            ] = pubkey
            addresses[
                str(
                    self.address_class.from_pubkey(
                        pubkey,
                        compressed=True,
                        version=0,
                        prefix=self.blockchain.prefix,
                    )
                )
            ] = pubkey
            addresses[
                str(
                    self.address_class.from_pubkey(
                        pubkey,
                        compressed=False,
                        version=56,
                        prefix=self.blockchain.prefix,
                    )
                )
            ] = pubkey
            addresses[
                str(
                    self.address_class.from_pubkey(
                        pubkey,
                        compressed=True,
                        version=56,
                        prefix=self.blockchain.prefix,
                    )
                )
            ] = pubkey

        if self["owner"] not in addresses.keys():
            raise MissingKeyError("Need key for address {}".format(self["owner"]))

        op = self.operations.Balance_claim(
            **{
                "fee": {"amount": 0, "asset_id": "1.3.0"},
                "deposit_to_account": account["id"],
                "balance_to_claim": self["id"],
                "balance_owner_key": addresses[self["owner"]],
                "total_claimed": self["balance"],
                "prefix": self.blockchain.prefix,
            }
        )
        signers = [
            account["name"],  # The fee payer and receiver account
            addresses.get(self["owner"]),  # The genesis balance!
        ]
        return self.blockchain.finalizeOp(op, signers, "active", **kwargs)