def sign(self):
        """ Sign a provided transaction with the provided key(s)

            :param dict tx: The transaction to be signed and returned
            :param string wifs: One or many wif keys to use for signing
                a transaction. If not present, the keys will be loaded
                from the wallet as defined in "missing_signatures" key
                of the transactions.
        """
        self.constructTx()

        if "operations" not in self or not self["operations"]:
            return

        # Legacy compatibility!
        # If we are doing a proposal, obtain the account from the proposer_id
        if self.blockchain.proposer:
            proposer = self.account_class(
                self.blockchain.proposer, blockchain_instance=self.blockchain
            )
            self.wifs = set()
            self.signing_accounts = list()
            self.appendSigner(proposer["id"], "active")

        # We need to set the default prefix, otherwise pubkeys are
        # presented wrongly!
        if self.blockchain.rpc:
            self.operations.default_prefix = self.blockchain.rpc.chain_params["prefix"]
        elif "blockchain" in self:
            self.operations.default_prefix = self["blockchain"]["prefix"]

        try:
            signedtx = self.signed_transaction_class(**self.json())
        except Exception:
            raise ValueError("Invalid TransactionBuilder Format")

        if not any(self.wifs):
            raise MissingKeyError

        signedtx.sign(self.wifs, chain=self.blockchain.rpc.chain_params)
        self["signatures"].extend(signedtx.json().get("signatures"))
        return signedtx